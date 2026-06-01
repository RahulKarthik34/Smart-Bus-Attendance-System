"""
DRF Serializers for Smart ID Card Scan Website

Replaces the old Pydantic models with Django REST Framework serializers.
Preserves the same validation logic (strip, uppercase, dangerous char detection).
"""
from rest_framework import serializers


# =====================================================
# Dangerous character validation (shared)
# =====================================================

DANGEROUS_CHARS = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]


def validate_no_dangerous_chars(value, field_name='Field'):
    """Check for SQL injection-like dangerous characters."""
    value = value.strip()
    if not value:
        raise serializers.ValidationError(f"{field_name} cannot be empty")
    if any(char in value.lower() for char in DANGEROUS_CHARS):
        raise serializers.ValidationError(f"Invalid characters in {field_name}")
    return value


# =====================================================
# Response Serializers
# =====================================================

class StudentResponseSerializer(serializers.Serializer):
    """Simple student ID response."""
    student_id = serializers.CharField()


class AttendanceResponseSerializer(serializers.Serializer):
    """Attendance save response."""
    success = serializers.BooleanField()
    message = serializers.CharField()
    timestamp = serializers.CharField(required=False, allow_null=True)
    student_id = serializers.CharField(required=False, allow_null=True)


# =====================================================
# Request Serializers
# =====================================================

class AttendanceSaveRequestSerializer(serializers.Serializer):
    """Request serializer for saving attendance."""
    student_id = serializers.CharField(min_length=1, max_length=50)
    bus_number = serializers.CharField(min_length=1, max_length=20)
    scan_type = serializers.ChoiceField(
        choices=['barcode', 'manual'],
        default='barcode'
    )
    role = serializers.ChoiceField(
        choices=['student', 'admin'],
        default='student'
    )
    auto_save = serializers.BooleanField(default=True)

    def validate_student_id(self, value):
        value = validate_no_dangerous_chars(value, 'Student ID')
        return value.upper()

    def validate_bus_number(self, value):
        value = validate_no_dangerous_chars(value, 'Bus Number')
        return value.upper()


class StudentCreateRequestSerializer(serializers.Serializer):
    """Request serializer for registering a new student."""
    student_id = serializers.CharField(min_length=1, max_length=20)
    name = serializers.CharField(min_length=1, max_length=100)
    roll_number = serializers.CharField(min_length=1, max_length=20)
    bus_number = serializers.CharField(min_length=1, max_length=20)

    def validate_student_id(self, value):
        value = validate_no_dangerous_chars(value, 'Student ID')
        return value.upper()

    def validate_name(self, value):
        return validate_no_dangerous_chars(value, 'Name')

    def validate_roll_number(self, value):
        value = validate_no_dangerous_chars(value, 'Roll Number')
        return value.upper()

    def validate_bus_number(self, value):
        value = validate_no_dangerous_chars(value, 'Bus Number')
        return value.upper()
