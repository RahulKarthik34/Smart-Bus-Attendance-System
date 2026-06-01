"""
Load SQL data into the database using Django ORM connection.

Usage:
    python load_data.py

Make sure to run from the backend/ directory.
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartid.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.db import connection


def load_data():
    """Load SQL data from the database/new_data.sql file."""
    backend_dir = os.path.dirname(__file__)
    file_path = os.path.join(os.path.dirname(backend_dir), 'database', 'new_data.sql')
    if not os.path.exists(file_path):
        file_path = os.path.join(os.path.dirname(backend_dir), 'database', 'schema.sql')
    
    print(f"Reading SQL file: {file_path}")

    if not os.path.exists(file_path):
        print(f"SQL file not found at: {file_path}")
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # Split by semicolon to separate statements
    statements = content.split(';')

    print(f"Found {len(statements)} potential statements.")

    count = 0
    with connection.cursor() as cursor:
        for statement in statements:
            if statement.strip():
                try:
                    # Remove comments
                    lines = statement.split('\n')
                    clean_lines = [l for l in lines if not l.strip().startswith('--')]
                    clean_stmt = '\n'.join(clean_lines).strip()

                    if clean_stmt:
                        print(f"Executing: {clean_stmt[:100]}...")
                        cursor.execute(clean_stmt)
                        count += 1
                except Exception as e:
                    print(f"Error executing statement: {e}")
                    # Don't exit, try next statement

    print(f"Successfully executed {count} statements.")


if __name__ == "__main__":
    # Test database connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        print("Database connected successfully.")
        load_data()
    except Exception as e:
        print(f"Could not connect to database: {e}")
        print("Please check credentials in backend/.env")
