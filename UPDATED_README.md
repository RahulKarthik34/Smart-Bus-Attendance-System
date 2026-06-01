# Smart ID Card Scan System (V2)

## 🆕 New Features Explanation

This updated version includes strict role-based access and time controls.

### ⏰ Strict Time Windows
- **Scanning**: 07:00 AM - 10:00 AM ONLY
- **Cleanup**: 06:00 PM (Auto-delete daily records)
- **Scans outside 7-10 AM will be rejected** by both Frontend and Backend.

### 👥 User Roles (No Login)

**1. Student Role**
- **Scan**: Can scan ID cards.
- **Save**: **AUTO-SAVE** enabled (2-second delay after preview).
- **View**: Cannot see full attendance list (Privacy).
- **Usage**: Walk up to kiosk, scan, wait for green "Success", leave.

**2. Admin Role**
- **Scan**: Can scan ID cards.
- **Save**: **MANUAL SAVE** required (Must click button).
- **View**: Can see **FULL** attendance list for today.
- **Usage**: Verify students manually, handle issues.

### 🧹 Auto-Cleanup
- A background scheduler (`scheduler.py`) must be running.
- Deletes all attendance data at **6:00 PM** every day.
- Keeps student master data safe.

## 🚀 How to Run

### 1. Start Backend Server
```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start Scheduler (New!)
Open a **new** terminal window:
```powershell
cd backend
python scheduler.py
```
*Keep this running to ensure 6:00 PM cleanup happens!*

### 3. Open Frontend
Open `frontend/index.html` in your browser.

## 🧪 Testing Tips
- **To test scanning**: If it's not currently 7-10 AM, you can temporarily edit `backend/config.py` time settings to testing hours.
- **To test roles**: Use the dropdown in top right corner.
