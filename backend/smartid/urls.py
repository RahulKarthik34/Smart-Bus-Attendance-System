"""
Smart ID Card Scan Website - Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin Panel (bonus feature from DRF migration)
    path('admin/', admin.site.urls),

    # All application URLs (root endpoints + /api/ endpoints)
    path('', include('attendance.urls')),
]
