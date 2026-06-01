"""
Django ORM Models for Smart ID Card Scan Website

Maps to the existing MySQL tables (students, attendance).
Uses managed = False so Django doesn't try to alter existing tables.
"""
from django.db import models


class Student(models.Model):
    """
    Student master data for ID card validation.
    Maps to the existing 'students' table.
    """
    objects = models.Manager()

    student_id = models.CharField(
        max_length=20,
        primary_key=True,
        db_comment='Unique student identifier from ID card'
    )
    name = models.CharField(
        max_length=100,
        db_comment='Full name of the student'
    )
    roll_number = models.CharField(
        max_length=20,
        unique=True,
        db_comment='Academic roll number'
    )
    bus_number = models.CharField(
        max_length=20,
        db_comment='Assigned bus number for transportation'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        managed = False  # Don't modify existing table
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.name}"


class Attendance(models.Model):
    """
    Daily attendance records with duplicate prevention.
    Maps to the existing 'attendance' table.
    """
    SCAN_TYPE_CHOICES = [
        ('barcode', 'Barcode'),
        ('manual', 'Manual'),
    ]

    objects = models.Manager()

    attendance_id = models.AutoField(
        primary_key=True,
        db_comment='Unique attendance record ID'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        db_column='student_id',
        db_comment='Foreign key to students table'
    )
    scan_date = models.DateField(
        db_comment='Date of attendance scan'
    )
    scan_time = models.TimeField(
        db_comment='Time of attendance scan'
    )
    scan_type = models.CharField(
        max_length=10,
        choices=SCAN_TYPE_CHOICES,
        default='barcode',
        db_comment='Type of scan performed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'attendance'
        managed = False  # Don't modify existing table
        unique_together = ('student', 'scan_date')
        ordering = ['-scan_time']

    def __str__(self):
        return f"{self.student_id} - {self.scan_date} {self.scan_time}"
