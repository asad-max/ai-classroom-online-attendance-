from django.urls import path
from .views import (
    MarkAttendanceView,
    MyAttendanceView,
    InstructorAttendanceHistoryView,
    ClassAttendanceView
)

urlpatterns = [
    path('mark/', MarkAttendanceView.as_view(), name='mark-attendance'),
    path('mine/', MyAttendanceView.as_view(), name='student-attendance-history'),
    path('instructor-history/', InstructorAttendanceHistoryView.as_view(), name='instructor-attendance-history'),
    path('class/<str:join_code>/', ClassAttendanceView.as_view(), name='class-attendance-history'),
   

]
