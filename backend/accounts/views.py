from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser


class MyFaceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Ensure this is a student with an uploaded face
        user = request.user
        if user.role != 'student' or not user.face_image:
            return Response({'error': 'No face image available.'}, status=404)

        return Response({
            'name': user.name,
            'image_url': request.build_absolute_uri(user.face_image.url)
        })

class FaceListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'instructor':
            return Response({'error': 'Unauthorized'}, status=403)

        students = CustomUser.objects.filter(role='student', face_image__isnull=False)
        data = [
            {
                "name": student.name,
                "image_url": request.build_absolute_uri(student.face_image.url)
            }
            for student in students
        ]
        return Response(data)

class RegisterView(APIView):
    # ✅ Do NOT require auth here
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ REQUIRED HERE

    def get(self, request):
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)
