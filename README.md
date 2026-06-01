<<<<<<< HEAD
# Smart ID Card Scan Website

A professional web-based attendance system that records attendance by scanning Barcode and QR codes from ID cards.

## Features

- **Scan ID Cards**: Support for barcode and QR code scanners (keyboard-emulated or camera-based)
- **Live Preview**: Display scanned student information before saving
- **Manual Confirmation**: Save attendance only after user confirmation
- **Duplicate Prevention**: Automatic duplicate detection for same-day attendance
- **Real-time Validation**: Instant feedback on scan status

## System Flow

1. **Scan ID Card** → Extract unique ID from barcode/QR code
2. **Display Preview** → Show student information (ID, name, bus number)
3. **Manual Save** → User clicks "Save" button to confirm
4. **Store in Database** → Save with validation and duplicate check

## Tech Stack

- **Backend**: Python 3.10+ with Django REST Framework
- **Database**: MySQL 8.0+
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Dependencies**: Django, DRF, django-cors-headers, mysql-connector-python

## Project Structure

```
id-card-project/
├── backend/
│   ├── manage.py              # Django management script
│   ├── requirements.txt
│   ├── .env                   # Environment variables
│   ├── smartid/               # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── attendance/            # Django app
│       ├── models.py          # Django ORM models
│       ├── serializers.py     # DRF serializers
│       ├── views.py           # DRF APIViews
│       ├── urls.py            # App routes
│       └── admin.py           # Django admin config
├── database/
│   ├── schema.sql             # Database schema
│   └── sample_data.sql        # Sample student data
├── frontend/
│   ├── index.html             # Main scan page
│   ├── css/
│   │   └── style.css          # Styling
│   └── js/
│       └── app.js             # Frontend logic
└── README.md
```

## Installation

### 1. Database Setup

```bash
# Create database
mysql -u root -p
CREATE DATABASE attendance_system;
USE attendance_system;

# Run schema
SOURCE database/schema.sql;
SOURCE database/sample_data.sql;
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Configure database connection in .env
# Edit DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

# Run backend
python manage.py runserver 0.0.0.0:8000
```

### 3. Frontend Setup

Simply open `frontend/index.html` in a web browser, or serve it using:

```bash
cd frontend
python -m http.server 8080
```

Visit: `http://localhost:8080`

## Usage

### Scanning ID Cards

1. **Focus Input Field**: Click on the scan input field
2. **Scan ID Card**: Use barcode/QR scanner to scan student ID
3. **View Preview**: Student information will display automatically
4. **Confirm Save**: Click "Save Attendance" button to record
5. **Status Message**: See confirmation or error message

### Scanner Types Supported

- **Keyboard-emulated scanners**: Scanners that type the ID like a keyboard
- **Camera-based scanners**: QR code readers using device camera
- **Manual entry**: Type ID manually for testing

## API Endpoints

### GET /api/student/{student_id}
Preview student information before saving

**Response:**
```json
{
  "student_id": "STU001",
  "name": "John Doe",
  "roll_number": "2024001",
  "bus_number": "BUS-05"
}
```

### POST /api/attendance/save
Save attendance after user confirmation

**Request:**
```json
{
  "student_id": "STU001",
  "scan_type": "barcode"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Attendance saved successfully",
  "timestamp": "2026-01-10 11:00:37"
}
```

## Security Features

- Input validation and sanitization
- SQL injection prevention using parameterized queries
- Duplicate attendance detection
- Error handling and logging

## Production Deployment

1. Use environment variables for sensitive data
2. Enable HTTPS for secure communication
3. Set up proper CORS policies
4. Configure MySQL with proper user permissions
5. Use a production WSGI server (Gunicorn)
6. Implement rate limiting for API endpoints
7. Access Django Admin at `/admin/` for data management

## License

MIT License - Feel free to use for educational and commercial purposes.
=======
# Smart-Bus-Attendance-System
A Smart Bus Attendance System built using Python and MySQL that automates student attendance through barcode scanning. The system captures student IDs in real time, logs attendance with timestamps, and stores records securely in a relational database, reducing manual effort and errors.
>>>>>>> bb712f427ecf27a6f0c21c6e08330735279b56d6
