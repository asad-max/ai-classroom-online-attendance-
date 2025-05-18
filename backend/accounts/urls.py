from django.urls import path
from .views import RegisterView, CurrentUserView, FaceListView, MyFaceView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('faces/', FaceListView.as_view(), name='faces'),  
    path('my-face/',  MyFaceView.as_view(), name='my-face'), 
]
