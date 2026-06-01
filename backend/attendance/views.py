"""
DRF Views for Smart ID Card Scan Website

Replaces the old FastAPI route handlers with Django REST Framework APIViews.
All endpoints preserve the exact same URL patterns and JSON response format
so the frontend works without any changes.
"""
from datetime import date, datetime, time as dt_time

from django.conf import settings
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import APIException

from .models import Student, Attendance
from .serializers import (
    StudentResponseSerializer,
    AttendanceResponseSerializer,
    AttendanceSaveRequestSerializer,
    StudentCreateRequestSerializer,
)


# =====================================================
# Custom Exception Handler (matching FastAPI format)
# =====================================================

def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns JSON responses
    matching the old FastAPI error format.
    """
    from rest_framework.views import exception_handler as default_handler
    response = default_handler(exc, context)

    if response is not None:
        # If DRF handled the exception, format it to match FastAPI's style
        detail = response.data.get('detail', str(response.data))
        response.data = {
            'success': False,
            'message': 'Error',
            'detail': detail,
        }
    else:
        # Unhandled exception — return 500
        print(f"Global exception: {exc}")
        detail = str(exc) if settings.DEBUG else 'An error occurred'
        response = Response(
            {
                'success': False,
                'message': 'Internal server error',
                'detail': detail,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


# =====================================================
# Helper Functions
# =====================================================

def is_within_scan_time():
    """
    Check if current time is within allowed scanning window.
    Returns (is_allowed: bool, message: str).
    """
    current_time = datetime.now().time()

    start_time = datetime.strptime(settings.SCAN_START_TIME, "%H:%M").time()
    end_time = datetime.strptime(settings.SCAN_END_TIME, "%H:%M").time()

    if settings.SKIP_TIME_CHECK:
        return True, "Time check skipped (Dev Mode)"

    if start_time <= current_time <= end_time:
        return True, "Within scanning window"
    else:
        return False, f"Scanning is only allowed between {settings.SCAN_START_TIME} and {settings.SCAN_END_TIME}."


# =====================================================
# GET /  — Root Endpoint
# =====================================================

class RootView(APIView):
    """Root endpoint with API information."""

    def get(self, request):
        return Response({
            'app_name': settings.APP_NAME,
            'version': settings.APP_VERSION,
            'status': 'running',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'docs': '/api/',
                'student_preview': '/api/student/{student_id}',
                'save_attendance': '/api/attendance/save',
                'today_attendance': '/api/attendance/today',
            },
        })


# =====================================================
# GET /health  — Health Check
# =====================================================

class HealthCheckView(APIView):
    """Health check endpoint for monitoring."""

    def get(self, request):
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            db_status = 'connected'
        except Exception:
            db_status = 'disconnected'

        return Response({
            'status': 'healthy' if db_status == 'connected' else 'unhealthy',
            'database': db_status,
            'timestamp': datetime.now().isoformat(),
        })


# =====================================================
# GET /api/student/{student_id}  — Student Preview
# =====================================================

class StudentPreviewView(APIView):
    """Get student ID for preview (bypasses database existence check)."""

    def get(self, request, student_id):
        # Check scanning time window
        is_allowed, time_message = is_within_scan_time()
        if not is_allowed:
            return Response(
                {'detail': time_message},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Sanitize input
        student_id = student_id.strip().upper()

        serializer = StudentResponseSerializer({'student_id': student_id})
        return Response(serializer.data)



# =====================================================
# POST /api/student/register  — Register Student
# =====================================================

class StudentRegisterView(APIView):
    """Register a new student in the students table."""

    def post(self, request):
        serializer = StudentCreateRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        student_id = data['student_id']
        name = data['name']
        roll_number = data['roll_number']
        bus_number = data['bus_number']

        # Check if student ID already exists
        if Student.objects.filter(student_id=student_id).exists():
            return Response(
                {'detail': f"Student ID '{student_id}' is already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if roll number already exists
        if Student.objects.filter(roll_number=roll_number).exists():
            return Response(
                {'detail': f"Roll Number '{roll_number}' is already registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Insert student record
        try:
            Student.objects.create(
                student_id=student_id,
                name=name,
                roll_number=roll_number,
                bus_number=bus_number,
            )
        except IntegrityError as e:
            print(f"Database error in register_student: {e}")
            return Response(
                {'detail': 'Failed to register student'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        response_data = {
            'success': True,
            'message': f'Student {name} registered successfully',
            'student_id': student_id,
        }
        return Response(response_data, status=status.HTTP_200_OK)


# =====================================================
# POST /api/attendance/save  — Save Attendance
# =====================================================

class AttendanceSaveView(APIView):
    """Save attendance directly (checks duplicate and DB constraints)."""

    def post(self, request):
        # Check scanning time window
        is_allowed, time_message = is_within_scan_time()
        if not is_allowed:
            return Response(
                {'detail': time_message},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AttendanceSaveRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        student_id = data['student_id']
        scan_type = data['scan_type']

        # Step 1: Get or create student automatically on the fly
        bus_number = data.get('bus_number')
        try:
            student, created = Student.objects.get_or_create(
                student_id=student_id,
                defaults={
                    'name': student_id,  # Default name to the ID/Roll Number
                    'roll_number': student_id,
                    'bus_number': bus_number,
                }
            )
            # Update student's bus number if it has changed
            if not created and student.bus_number != bus_number:
                student.bus_number = bus_number
                student.save()
        except Exception as e:
            print(f"Error resolving student in save_attendance: {e}")
            # Fallback in case of duplicate unique constraints or database issues
            student = Student.objects.filter(student_id=student_id).first()
            if not student:
                student = Student.objects.filter(roll_number=student_id).first()
            
            if student:
                if student.bus_number != bus_number:
                    student.bus_number = bus_number
                    student.save()
            else:
                return Response(
                    {'detail': 'Failed to save or resolve student in database'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )


        # Step 2: Check for duplicate attendance today
        today = date.today()
        existing = Attendance.objects.filter(
            student_id=student_id,
            scan_date=today,
        ).first()

        if existing:
            return Response(
                {'detail': f"Attendance already marked today at {existing.scan_time}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Step 3: Save attendance
        current_time = datetime.now()
        try:
            Attendance.objects.create(
                student=student,
                scan_date=today,
                scan_time=current_time.time(),
                scan_type=scan_type,
            )
        except IntegrityError as e:
            print(f"Database error in save_attendance: {e}")
            return Response(
                {'detail': 'Failed to save attendance'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Step 4: Return success response
        response_data = {
            'success': True,
            'message': 'Attendance saved successfully',
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S'),
            'student_id': student_id,
        }
        return Response(response_data, status=status.HTTP_200_OK)


# =====================================================
# GET /api/attendance/today  — Today's Attendance
# =====================================================

class TodayAttendanceView(APIView):
    """Get list of IDs who marked attendance today."""

    def get(self, request):
        role = request.query_params.get('role', 'student')
        student_id = request.query_params.get('student_id', None)

        if role == 'student':
            if not student_id:
                return Response(
                    {'detail': 'student_id is required for student role'},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            records = Attendance.objects.filter(
                student_id=student_id.upper(),
                scan_date=date.today(),
            ).select_related('student').order_by('-scan_time')
        else:
            records = Attendance.objects.filter(
                scan_date=date.today(),
            ).select_related('student').order_by('-scan_time')

        # Format results matching the old API response
        attendance_list = []
        for record in records:
            scan_time_val = record.scan_time
            if isinstance(scan_time_val, (dt_time, datetime)):
                scan_time_str = scan_time_val.strftime('%H:%M:%S')
            else:
                scan_time_str = str(scan_time_val)

            attendance_list.append({
                'student_id': record.student_id,
                'bus_number': record.student.bus_number,
                'scan_time': scan_time_str,
                'scan_type': record.scan_type,
            })

        return Response({
            'date': date.today().isoformat(),
            'total_present': len(attendance_list),
            'attendance_list': attendance_list,
        })


# =====================================================
# DELETE /api/attendance/cleanup  — Daily Cleanup
# =====================================================

class AttendanceCleanupView(APIView):
    """Delete all attendance records for daily cleanup."""

    def delete(self, request):
        try:
            Attendance.objects.all().delete()
            return Response({
                'success': True,
                'message': 'Daily attendance cleanup completed',
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            })
        except Exception as e:
            print(f"Database error in cleanup_daily_attendance: {e}")
            return Response(
                {'detail': 'Failed to cleanup attendance data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
