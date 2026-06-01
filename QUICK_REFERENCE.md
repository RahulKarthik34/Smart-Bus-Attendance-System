# Quick Reference Card

## 🚀 Start Commands

### Backend
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```powershell
cd frontend
python -m http.server 8080
# OR just open index.html
```

---

## 🔗 Important URLs

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/student/{id}` | Preview student info |
| POST | `/api/attendance/save` | Save attendance |
| GET | `/api/attendance/today` | Get today's list |
| GET | `/health` | System health |

---

## 🧪 Test Student IDs

- `STU001` - Rahul Sharma (BUS-05)
- `STU002` - Priya Patel (BUS-03)
- `STU003` - Amit Kumar (BUS-05)
- `STU004` - Sneha Reddy (BUS-07)
- `STU005` - Vikram Singh (BUS-02)

---

## 🔧 Configuration

**File**: `backend/config.py`

```python
DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = "root"
DB_PASSWORD = "YOUR_PASSWORD"  # ← Change this
DB_NAME = "attendance_system"
```

---

## 💾 Database Setup

```sql
-- Create database
CREATE DATABASE attendance_system;
USE attendance_system;

-- Load schema
SOURCE database/schema.sql;

-- Load sample data
SOURCE database/sample_data.sql;

-- Verify
SELECT COUNT(*) FROM students;  -- Should be 20
```

---

## 🐛 Common Issues

### Backend won't start
```powershell
# Install dependencies
pip install -r requirements.txt
```

### Database connection failed
```powershell
# Check MySQL is running
mysql -u root -p

# Verify credentials in config.py
```

### Frontend shows "CORS error"
```powershell
# Make sure backend is running
# Check backend terminal for startup messages
```

---

## 📊 System Flow

```
1. SCAN → 2. PREVIEW → 3. CLICK SAVE → 4. DATABASE
```

**Important**: Nothing saves until user clicks "Save Attendance"!

---

## ✅ Testing Checklist

- [ ] Backend running (port 8000)
- [ ] Frontend accessible
- [ ] Database connected
- [ ] Health check returns "healthy"
- [ ] Can scan student ID
- [ ] Preview shows correctly
- [ ] Can save attendance
- [ ] Duplicate prevention works
- [ ] Attendance list updates

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `backend/app/main.py` | FastAPI app |
| `backend/app/routes/attendance.py` | API endpoints |
| `backend/config.py` | Database config |
| `frontend/index.html` | Main page |
| `frontend/js/app.js` | Frontend logic |
| `database/schema.sql` | Database schema |

---

## 📞 Quick Help

**Check system status**:
```powershell
# Visit health endpoint
curl http://localhost:8000/health
```

**View API docs**:
```
http://localhost:8000/docs
```

**Test API directly**:
```powershell
# Preview student
curl http://localhost:8000/api/student/STU001

# Save attendance (requires JSON)
curl -X POST http://localhost:8000/api/attendance/save \
  -H "Content-Type: application/json" \
  -d '{"student_id":"STU001","scan_type":"barcode"}'
```

---

## 🎯 Default Ports

- Backend: **8000**
- Frontend: **8080** (or direct file access)
- MySQL: **3306**

---

## 📚 Documentation Files

- `README.md` - Main documentation
- `SETUP_GUIDE.md` - Detailed setup
- `SYSTEM_FLOW.md` - Flow explanation
- `PROJECT_SUMMARY.md` - Complete overview
- `QUICK_REFERENCE.md` - This file

---

**For detailed help, see SETUP_GUIDE.md**
