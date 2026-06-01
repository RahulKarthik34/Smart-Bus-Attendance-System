-- =====================================================
-- Smart ID Card Scan Website - Database Schema
-- =====================================================
-- Description: MySQL schema for attendance tracking system
-- Created: 2026-01-10
-- =====================================================

-- Drop existing tables if they exist
DROP TABLE IF EXISTS attendance;
DROP TABLE IF EXISTS students;

-- =====================================================
-- Students Table
-- =====================================================
-- Stores student information for ID card validation
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY COMMENT 'Unique student identifier from ID card',
    name VARCHAR(100) NOT NULL COMMENT 'Full name of the student',
    roll_number VARCHAR(20) NOT NULL UNIQUE COMMENT 'Academic roll number',
    bus_number VARCHAR(20) NOT NULL COMMENT 'Assigned bus number for transportation',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record last update timestamp',
    
    INDEX idx_roll_number (roll_number),
    INDEX idx_bus_number (bus_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Student master data for ID card validation';

-- =====================================================
-- Attendance Table
-- =====================================================
-- Records daily attendance scans with duplicate prevention
CREATE TABLE attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique attendance record ID',
    student_id VARCHAR(20) NOT NULL COMMENT 'Foreign key to students table',
    scan_date DATE NOT NULL COMMENT 'Date of attendance scan',
    scan_time TIME NOT NULL COMMENT 'Time of attendance scan',
    scan_type ENUM('barcode', 'manual') NOT NULL DEFAULT 'barcode' COMMENT 'Type of scan performed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation timestamp',
    
    -- Foreign key constraint to ensure data integrity
    CONSTRAINT fk_student_attendance 
        FOREIGN KEY (student_id) 
        REFERENCES students(student_id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Unique constraint to prevent duplicate attendance on same day
    CONSTRAINT unique_daily_attendance 
        UNIQUE (student_id, scan_date),
    
    -- Indexes for performance optimization
    INDEX idx_scan_date (scan_date),
    INDEX idx_student_date (student_id, scan_date),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
COMMENT='Daily attendance records with duplicate prevention';

-- =====================================================
-- Views for Reporting
-- =====================================================

-- Today's attendance summary
CREATE OR REPLACE VIEW today_attendance AS
SELECT 
    a.attendance_id,
    a.student_id,
    s.name,
    s.roll_number,
    s.bus_number,
    a.scan_time,
    a.scan_type
FROM attendance a
INNER JOIN students s ON a.student_id = s.student_id
WHERE a.scan_date = CURDATE()
ORDER BY a.scan_time DESC;

-- Attendance statistics
CREATE OR REPLACE VIEW attendance_stats AS
SELECT 
    scan_date,
    COUNT(DISTINCT student_id) as total_present,
    COUNT(CASE WHEN scan_type = 'barcode' THEN 1 END) as barcode_scans,
    COUNT(CASE WHEN scan_type = 'qrcode' THEN 1 END) as qrcode_scans,
    COUNT(CASE WHEN scan_type = 'manual' THEN 1 END) as manual_entries
FROM attendance
GROUP BY scan_date
ORDER BY scan_date DESC;

-- =====================================================
-- Sample Queries for Testing
-- =====================================================

-- Check if student has already marked attendance today
-- SELECT COUNT(*) FROM attendance 
-- WHERE student_id = 'STU001' AND scan_date = CURDATE();

-- Get today's attendance count
-- SELECT COUNT(*) as present_today FROM today_attendance;

-- Get attendance by bus number
-- SELECT * FROM today_attendance WHERE bus_number = 'BUS-05';
