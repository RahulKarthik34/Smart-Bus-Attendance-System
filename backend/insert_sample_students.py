"""
Insert sample student data into the database.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartid.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from attendance.models import Student

def insert_samples():
    sample_students = [
        {
            "student_id": "22KT1A0501",
            "name": "Rahul Sharma",
            "roll_number": "22KT1A0501",
            "bus_number": "05"
        },
        {
            "student_id": "22KT1A0502",
            "name": "John Doe",
            "roll_number": "22KT1A0502",
            "bus_number": "03"
        },
        {
            "student_id": "22KT1A0503",
            "name": "Jane Smith",
            "roll_number": "22KT1A0503",
            "bus_number": "12"
        },
        {
            "student_id": "22KT1A0504",
            "name": "Aravind Swamy",
            "roll_number": "22KT1A0504",
            "bus_number": "05"
        }
    ]

    print("Inserting sample students...")
    created_count = 0
    for student_data in sample_students:
        student, created = Student.objects.get_or_create(
            student_id=student_data["student_id"],
            defaults={
                "name": student_data["name"],
                "roll_number": student_data["roll_number"],
                "bus_number": student_data["bus_number"]
            }
        )
        if created:
            print(f"Created student: {student.name} ({student.student_id})")
            created_count += 1
        else:
            print(f"Student already exists: {student.name} ({student.student_id})")

    print(f"Insertion complete. Created {created_count} new student records.")

if __name__ == "__main__":
    insert_samples()
