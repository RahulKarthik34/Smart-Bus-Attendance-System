# Quick Setup Guide - Smart ID Card Scan Website

This guide will help you set up and run the attendance system in just a few minutes.

## Prerequisites

- **Python 3.8+** installed
- **MySQL 8.0+** installed and running
- **Web browser** (Chrome, Firefox, Edge, etc.)
- **Barcode/QR scanner** (optional - can use keyboard for testing)

## Step-by-Step Setup

### 1. Database Setup (5 minutes)

Open MySQL command line or MySQL Workbench:

```sql
-- Create database
CREATE DATABASE attendance_system;

-- Use the database
USE attendance_system;

-- Run the schema file
SOURCE C:/Users/rahul/OneDrive/Documents/id card project/database/schema.sql;

-- Insert sample data
SOURCE C:/Users/rahul/OneDrive/Documents/id card project/database/sample_data.sql;

-- Verify setup
SELECT COUNT(*) as total_students FROM students;
-- Should show 20 students
```

### 2. Backend Configuration (2 minutes)

Edit the file: `backend/config.py`

Update these lines with your MySQL credentials:

```python
DB_HOST: str = os.getenv("DB_HOST", "localhost")
DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
DB_USER: str = os.getenv("DB_USER", "root")
DB_PASSWORD: str = os.getenv("DB_PASSWORD", "YOUR_MYSQL_PASSWORD_HERE")  # <-- CHANGE THIS
DB_NAME: str = os.getenv("DB_NAME", "attendance_system")
```

### 3. Install Python Dependencies (3 minutes)

Open PowerShell in the project directory:

```powershell
cd "C:\Users\rahul\OneDrive\Documents\id card project\backend"

# Install dependencies
pip install -r requirements.txt
```

### 4. Start Backend Server (1 minute)

```powershell
# Make sure you're in the backend directory
cd "C:\Users\rahul\OneDrive\Documents\id card project\backend"

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
✓ Database connected successfully
📝 API Documentation: http://localhost:8000/docs
```

**Keep this terminal window open!**

### 5. Open Frontend (1 minute)

**Option A: Direct File Access**
- Navigate to: `C:\Users\rahul\OneDrive\Documents\id card project\frontend`
- Double-click `index.html`

**Option B: Local Server (Recommended)**

Open a NEW PowerShell window:

```powershell
cd "C:\Users\rahul\OneDrive\Documents\id card project\frontend"

# Start simple HTTP server
python -m http.server 8080
```

Then open browser: `http://localhost:8080`

## Testing the System

### Manual Testing (No Scanner Required)

1. Click in the scan input field
2. Type a student ID (e.g., `STU001`)
3. Press **Enter**
4. Review the student preview
5. Click **"Save Attendance"**
6. See success message and attendance list update

### Sample Student IDs for Testing

- `22KT1A0501` - Abhishek Sharma (BUS-10)
- `22KT1A0502` - Bhavya Sri (BUS-12)
- `22KT1A0503` - Chaitanya Kumar (BUS-05)
- `22KT1A0504` - Deepika Rani (BUS-08)
- `22KT1A0505` - Eshwar Rao (BUS-10)

### Test Duplicate Prevention

1. Scan `STU001` and save attendance
2. Try to scan `STU001` again
3. You should see: **"Attendance already marked today"**

### With Physical Scanner

1. Configure your barcode/QR scanner to act as keyboard input
2. Click the scan input field
3. Scan any ID card with student ID
4. System will auto-process when scanner sends Enter key

## Troubleshooting

### Backend Issues

**"Database connection failed"**
- Check MySQL is running
- Verify credentials in `config.py`
- Test connection: `mysql -u root -p`

**"Module not found"**
- Run: `pip install -r requirements.txt`
- Make sure you're in the `backend` directory

### Frontend Issues

**"Failed to fetch"**
- Make sure backend is running on port 8000
- Check browser console (F12) for errors
- Verify CORS is enabled in backend

**"Student not found"**
- Check database has sample data
- Run: `SELECT * FROM students;` in MySQL

### Port Already in Use

**Backend (port 8000)**
```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
# Update frontend API_BASE_URL in js/app.js
```

**Frontend (port 8080)**
```powershell
python -m http.server 8081
```

## Verify Everything Works

✅ **Backend Health Check**
- Open: `http://localhost:8000/health`
- Should show: `{"status":"healthy","database":"connected"}`

✅ **API Documentation**
- Open: `http://localhost:8000/docs`
- Interactive API testing interface

✅ **Frontend Loading**
- Open frontend URL
- Should see "Smart ID Card Scan" header
- Status badge should show "Ready"

✅ **Complete Flow Test**
1. Scan/type student ID
2. See preview with student details
3. Click "Save Attendance"
4. See success message
5. See attendance appear in table below

## Production Deployment Notes

When deploying to production:

1. **Environment Variables**: Use `.env` file for sensitive data
2. **HTTPS**: Enable SSL/TLS certificates
3. **CORS**: Restrict allowed origins in `config.py`
4. **Database**: Use environment-specific credentials
5. **Server**: Use Gunicorn instead of Uvicorn directly
6. **Monitoring**: Add logging and error tracking

## Need Help?

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Database Check**: `mysql -u root -p attendance_system`

---

**That's it! Your attendance system is ready to use! 🎉**
