from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ClassRoom
from .serializers import ClassRoomSerializer

class CreateClassView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ClassRoomSerializer

    def perform_create(self, serializer):
        if self.request.user.role != 'instructor':
            raise PermissionError("Only instructors can create classes.")
        serializer.save(instructor=self.request.user)

class JoinClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('join_code')
        try:
            classroom = ClassRoom.objects.get(join_code=code)
            classroom.students.add(request.user)
            return Response({"message": "✅ Joined class successfully."})
        except ClassRoom.DoesNotExist:
            return Response({"error": "❌ Invalid join code."}, status=400)

class MyClassesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'instructor':
            classes = ClassRoom.objects.filter(instructor=request.user)
        else:
            classes = request.user.joined_classes.all()
        data = ClassRoomSerializer(classes, many=True).data
        return Response(data)
    

class ToggleLiveStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get('join_code')
        try:
            classroom = ClassRoom.objects.get(join_code=code, instructor=request.user)
            classroom.is_live = not classroom.is_live
            classroom.save()
            status_msg = "started" if classroom.is_live else "ended"
            return Response({"message": f"📡 Class {status_msg}."})
        except ClassRoom.DoesNotExist:
            return Response({"error": "❌ Class not found or unauthorized."}, status=403)
