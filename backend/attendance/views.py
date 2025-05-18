from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Attendance
from classes.models import ClassRoom
from accounts.models import CustomUser

class ClassAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, join_code):
        # Ensure instructor only can view this class history
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can access this."}, status=403)

        try:
            classroom = ClassRoom.objects.get(join_code=join_code, instructor=request.user)
        except ClassRoom.DoesNotExist:
            return Response({"error": "Class not found or you do not have permission."}, status=404)

        records = Attendance.objects.filter(classroom=classroom).select_related('student')

        data = [
            {
                "student": a.student.name,
                "email": a.student.email,
                "timestamp": a.timestamp,
            }
            for a in records
        ]

        return Response(data, status=200)

class InstructorAttendanceHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'instructor':
            return Response({'error': 'Unauthorized'}, status=403)

        classes = ClassRoom.objects.filter(instructor=request.user)
        history = []

        for cls in classes:
            records = Attendance.objects.filter(classroom=cls).select_related('student')
            for rec in records:
                history.append({
                    'class_name': cls.name,
                    'subject_code': cls.subject_code,
                    'student_name': rec.student.name,
                    'timestamp': rec.timestamp,
                })

        return Response(history)


class MarkAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name      = request.data.get('name')
        join_code = request.data.get('join_code')

        # 1) Find the ClassRoom
        try:
            classroom = ClassRoom.objects.get(join_code=join_code)
        except ClassRoom.DoesNotExist:
            return Response({'error': 'Invalid class code.'}, status=400)

        # 2) Find the student by name
        try:
            student = CustomUser.objects.get(name=name, role='student')
        except CustomUser.DoesNotExist:
            return Response({'error': 'Student not registered.'}, status=400)

        # 3) Create or update attendance record
        Attendance.objects.update_or_create(
            classroom=classroom,
            student=student,
            defaults={'timestamp': timezone.now()}
        )

        return Response({'message': 'Attendance marked.'}, status=200)
# attendance/views.py
class MyAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role != 'student':
            return Response({"error": "Not allowed"}, status=403)

        records = Attendance.objects.filter(student=user).select_related("classroom")
        data = [
            {
                "class": a.classroom.name,
                "subject_code": a.classroom.subject_code,
                "timestamp": a.timestamp
            }
            for a in records
        ]
        return Response(data)
