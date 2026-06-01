"""
Django Admin Configuration for Smart ID Card Scan Website

Register models here to manage students and attendance
via the Django Admin panel at /admin/
"""
from django.contrib import admin
from .models import Student, Attendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin interface for Student model."""
    list_display = ('student_id', 'name', 'roll_number', 'bus_number', 'created_at')
    search_fields = ('student_id', 'name', 'roll_number')
    list_filter = ('bus_number',)
    ordering = ('student_id',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin interface for Attendance model."""
    list_display = ('attendance_id', 'student_id', 'scan_date', 'scan_time', 'scan_type')
    search_fields = ('student__student_id', 'student__name')
    list_filter = ('scan_date', 'scan_type')
    ordering = ('-scan_date', '-scan_time')
