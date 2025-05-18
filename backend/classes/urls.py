from django.urls import path
from .views import CreateClassView, JoinClassView, MyClassesView, ToggleLiveStatusView

urlpatterns = [
    path('create/', CreateClassView.as_view(), name='create-class'),
    path('join/', JoinClassView.as_view(), name='join-class'),
    path('mine/', MyClassesView.as_view(), name='my-classes'),
    path('toggle-live/', ToggleLiveStatusView.as_view(), name='toggle-live'),
   
]

# Include in project URLs (ai_attendance/urls.py)





