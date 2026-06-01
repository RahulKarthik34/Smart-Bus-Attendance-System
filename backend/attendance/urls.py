"""
Attendance App URL Configuration

Preserves the exact same URL patterns as the old FastAPI routes
so the frontend works without any changes.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Root endpoints (no /api/ prefix)
    path('', views.RootView.as_view(), name='root'),
    path('health', views.HealthCheckView.as_view(), name='health-check'),

    # Student endpoints
    path('api/student/register', views.StudentRegisterView.as_view(), name='student-register'),
    path('api/student/<str:student_id>', views.StudentPreviewView.as_view(), name='student-preview'),

    # Attendance endpoints
    path('api/attendance/save', views.AttendanceSaveView.as_view(), name='attendance-save'),
    path('api/attendance/today', views.TodayAttendanceView.as_view(), name='attendance-today'),
    path('api/attendance/cleanup', views.AttendanceCleanupView.as_view(), name='attendance-cleanup'),
]
