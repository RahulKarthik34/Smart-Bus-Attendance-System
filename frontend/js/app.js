// =====================================================
// Smart ID Card Scan Website - Frontend Logic
// =====================================================

// Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',
    AUTO_CLEAR_TIMEOUT: 3000, // Clear status messages after 3 seconds
    SCAN_INPUT_CLEAR_DELAY: 300, // Delay before clearing scan input
    SCAN_START_HOUR: 0, // 12:00 AM
    SCAN_END_HOUR: 24,  // 12:00 AM (Next Day)
    DEV_MODE: true, // Bypass time restrictions
};

// State management
const state = {
    currentStudentData: null,
    currentScanType: 'barcode',
    role: 'student', // Default role
    isProcessing: false,
    html5QrcodeScanner: null,
    isCameraRunning: false,
    lastScannedId: localStorage.getItem('lastScannedId') || null
};

// =====================================================
// DOM Elements
// =====================================================
const elements = {
    // Scan section
    scanInput: document.getElementById('scanInput'),
    scanTypeRadios: document.querySelectorAll('input[name="scanType"]'),
    toggleCameraBtn: document.getElementById('toggleCameraBtn'), // New
    submitScanBtn: document.getElementById('submitScanBtn'), // New
    busNumberInput: document.getElementById('busNumberInput'), // New
    reader: document.getElementById('reader'), // New

    // Role selector
    roleSelect: document.getElementById('roleSelect'),

    // Preview section
    previewSection: document.getElementById('previewSection'),
    previewStudentId: document.getElementById('previewStudentId'),
    previewBusNumber: document.getElementById('previewBusNumber'),

    // Buttons
    saveBtn: document.getElementById('saveBtn'),
    cancelBtn: document.getElementById('cancelBtn'),
    refreshBtn: document.getElementById('refreshBtn'),

    // Status section
    statusSection: document.getElementById('statusSection'),
    statusMessage: document.getElementById('statusMessage'),
    statusIcon: document.getElementById('statusIcon'),
    statusTitle: document.getElementById('statusTitle'),
    statusDescription: document.getElementById('statusDescription'),

    // Attendance table
    attendanceTableBody: document.getElementById('attendanceTableBody'),
    todayCount: document.getElementById('todayCount'),
    systemStatus: document.getElementById('systemStatus'),
    inputWrapper: document.querySelector('.input-wrapper'),
    // Registration modal elements
    registerModal: document.getElementById('registerModal'),
    closeModalBtn: document.getElementById('closeModalBtn'),
    regCancelBtn: document.getElementById('regCancelBtn'),
    registerForm: document.getElementById('registerForm'),
    regStudentId: document.getElementById('regStudentId'),
    regStudentName: document.getElementById('regStudentName'),
    regRollNumber: document.getElementById('regRollNumber'),
    regBusNumber: document.getElementById('regBusNumber'),
};

// =====================================================
// Event Listeners
// =====================================================

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ Smart ID Card Scan System Initialized');

    // Initialize role
    if (elements.roleSelect) {
        state.role = elements.roleSelect.value;
    }

    // Auto-focus scan input
    elements.scanInput.focus();

    // Load today's attendance
    loadTodayAttendance();

    // Check system health
    checkSystemHealth();

    // Initial Manual Entry Visibility
    if (elements.inputWrapper) {
        elements.inputWrapper.style.display = 'flex'; // Visible by default
    }
});

// Role selector
if (elements.roleSelect) {
    elements.roleSelect.addEventListener('change', (e) => {
        state.role = e.target.value;
        console.log(`Role switched to: ${state.role}`);
        elements.scanInput.focus();
        loadTodayAttendance(); // Reload list based on new role
        resetForm();
    });
}

// Scan input - Listen for Enter key or scanner input
elements.scanInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !state.isProcessing) {
        e.preventDefault();
        handleScan();
    }
});

// Submit Button
if (elements.submitScanBtn) {
    elements.submitScanBtn.addEventListener('click', () => {
        handleScan();
    });
}

// Camera Toggle Button
if (elements.toggleCameraBtn) {
    elements.toggleCameraBtn.addEventListener('click', toggleCamera);
}

// Scan type selection
elements.scanTypeRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        state.currentScanType = e.target.value;
        console.log(`Scan type changed to: ${state.currentScanType}`);

        // Show typing bar ONLY for manual entry
        if (state.currentScanType === 'manual') {
            if (elements.inputWrapper) elements.inputWrapper.style.display = 'flex';
            elements.scanInput.focus();
        } else {
            if (elements.inputWrapper) elements.inputWrapper.style.display = 'none';
        }
    });
});

// Save button
elements.saveBtn.addEventListener('click', async () => {
    await saveAttendance();
});

// Cancel button
elements.cancelBtn.addEventListener('click', () => {
    resetForm();
});

// Refresh button
elements.refreshBtn.addEventListener('click', () => {
    loadTodayAttendance();
});

// Modal event listeners
if (elements.closeModalBtn) {
    elements.closeModalBtn.addEventListener('click', closeRegisterModal);
}
if (elements.regCancelBtn) {
    elements.regCancelBtn.addEventListener('click', closeRegisterModal);
}
if (elements.registerForm) {
    elements.registerForm.addEventListener('submit', submitStudentRegistration);
}

// =====================================================
// Core Functions
// =====================================================

/**
 * Toggle Camera
 */
function toggleCamera() {
    if (state.isCameraRunning) {
        stopCamera();
    } else {
        // If starting camera, hide manual input
        if (elements.inputWrapper) elements.inputWrapper.style.display = 'none';
        const manualRadio = document.querySelector('input[name="scanType"][value="manual"]');
        if (manualRadio) manualRadio.checked = false;
        state.currentScanType = 'barcode'; // Camera is always barcode/scan

        startCamera();
    }
}

function startCamera() {
    elements.reader.style.display = 'block';
    state.isCameraRunning = true;

    // UI Update
    elements.toggleCameraBtn.innerHTML = `
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
        Stop Camera
    `;
    elements.toggleCameraBtn.classList.remove('btn-secondary');
    elements.toggleCameraBtn.classList.add('btn-primary'); // Highlight active

    if (!state.html5QrcodeScanner) {
        // Initialize scanner
        state.html5QrcodeScanner = new Html5QrcodeScanner(
            "reader",
            {
                fps: 10,
                qrbox: { width: 250, height: 250 },
                showImageFileMenu: false, // Hide the "Scan Image File" option
                supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA] // Only allow camera scan
            },
            /* verbose= */ false
        );

        state.html5QrcodeScanner.render(onScanSuccess, onScanFailure);
    }
}

function stopCamera() {
    if (state.html5QrcodeScanner) {
        state.html5QrcodeScanner.clear().then(_ => {
            elements.reader.style.display = 'none';
            state.isCameraRunning = false;
            state.html5QrcodeScanner = null; // Reset to re-init next time

            // UI Update
            elements.toggleCameraBtn.innerHTML = `
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
                    <circle cx="12" cy="13" r="4"></circle>
                </svg>
                Scan ID
            `;
            elements.toggleCameraBtn.classList.add('btn-primary');
            elements.toggleCameraBtn.classList.remove('btn-secondary');
        }).catch(error => {
            console.error("Failed to stop camera", error);
        });
    }
}

function onScanSuccess(decodedText, decodedResult) {
    // Handle the scanned code
    console.log(`Scan result: ${decodedText}`, decodedResult);

    // Fill input
    elements.scanInput.value = decodedText;

    // Optionally stop camera automatically
    // stopCamera(); // User might want to keep scanning? Let's leave it running or stop?
    // Usually better to stop to indicate success? 
    // Let's stop if successful to show preview.
    stopCamera();

    // Show input fields so student can enter bus number
    if (elements.inputWrapper) elements.inputWrapper.style.display = 'flex';
    elements.busNumberInput.focus();

    // Trigger scan logic (which will prompt for bus number if empty)
    state.currentScanType = 'barcode';
    handleScan();
}

function onScanFailure(error) {
    // handle scan failure, usually better to ignore and keep scanning.
    // console.warn(`Code scan error = ${error}`);
}

/**
 * Check if current time is within allowed window
 * @returns {boolean} true if allowed
 */
function checkTimeWindow() {
    // Restriction removed as per user request
    const isAllowed = true;

    const banner = document.getElementById('timeWarningBanner');

    if (!isAllowed) {
        // Show Warning
        if (banner) banner.style.display = 'block';

        // Disable Input
        elements.scanInput.disabled = true;
        elements.scanInput.classList.add('input-disabled');
        elements.scanInput.placeholder = 'Scanning Paused (07:00 - 10:00 AM only)';

        // Disable new buttons
        if (elements.submitScanBtn) elements.submitScanBtn.disabled = true;
        if (elements.toggleCameraBtn) elements.toggleCameraBtn.disabled = true;

    } else {
        // Hide Warning
        if (banner) banner.style.display = 'none';

        // Enable Input
        elements.scanInput.disabled = false;
        elements.scanInput.classList.remove('input-disabled');
        elements.scanInput.placeholder = 'Scan Barcode / QR Code';

        // Enable new buttons
        if (elements.submitScanBtn) elements.submitScanBtn.disabled = false;
        if (elements.toggleCameraBtn) elements.toggleCameraBtn.disabled = false;
    }

    return isAllowed;
}

/**
 * Handle ID card scan
 */
async function handleScan() {
    // 1. Time Window Check
    if (!checkTimeWindow()) {
        showStatus('error', 'Scanning Closed', `ID scanning allowed only between ${CONFIG.SCAN_START_HOUR}:00 AM and ${CONFIG.SCAN_END_HOUR}:00 AM.`);
        elements.scanInput.value = '';
        return;
    }

    const studentId = elements.scanInput.value.trim().toUpperCase();
    const busNumber = elements.busNumberInput.value.trim().toUpperCase();

    // Validation
    if (!studentId) {
        showStatus('error', 'Invalid Input', 'Please scan or enter a valid student ID');
        return;
    }

    if (!busNumber) {
        showStatus('error', 'Invalid Input', 'Please enter a bus number to continue');
        elements.busNumberInput.focus();
        return;
    }

    if (state.isProcessing) return;
    state.isProcessing = true;

    try {
        showStatus('info', 'Processing...', 'Fetching student information');

        // Fetch student preview data
        const response = await fetch(`${CONFIG.API_BASE_URL}/student/${studentId}`);

        if (!response.ok) {
            const errData = await response.json();
            if (response.status === 403) {
                throw new Error(errData.detail || 'Scanning outside allowed hours');
            }
            if (response.status === 404) {
                // Suppress global status message and show registration modal
                elements.statusSection.style.display = 'none';
                showRegisterModal(studentId, busNumber);
                return;
            }
            throw new Error('Failed to fetch student information');
        }

        const studentData = await response.json();
        // Manually add bus number to student data for preview
        studentData.bus_number = busNumber;
        state.currentStudentData = studentData;

        // Track the mode for auto-restart
        state.lastUsedMode = state.isCameraRunning ? 'camera' : 'manual';

        // Display preview
        displayPreview(studentData);

        // Hide status message
        elements.statusSection.style.display = 'none';

        // Clear input
        setTimeout(() => {
            elements.scanInput.value = '';
        }, CONFIG.SCAN_INPUT_CLEAR_DELAY);

    } catch (error) {
        console.error('✗ Scan error:', error);
        showStatus('error', 'Scan Failed', error.message);
        elements.scanInput.value = '';
        elements.scanInput.focus();
    } finally {
        state.isProcessing = false;
    }
}



/**
 * Display student preview
 */
function displayPreview(studentData) {
    elements.previewStudentId.textContent = studentData.student_id;
    elements.previewBusNumber.textContent = studentData.bus_number;
    elements.previewSection.style.display = 'block';
    elements.previewSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // If student role, hide the manual save/cancel buttons to prevent confusion during auto-save?
    // User requirement says "Manual Save Action: Provide a Save / Confirm button". 
    // But updated rule says "Attendance is saved automatically or by admin confirmation".
    // I will keep buttons visible so student can Cancel quickly if wrong scan.
}

/**
 * Save attendance
 * @param {boolean} isAutoSave - flag for auto-save
 */
async function saveAttendance(isAutoSave = false) {
    if (!state.currentStudentData) return;

    // processing flag is already handled in handleScan usually, but we need it here for manual click
    // If called from auto-save, we are in a timeout, so we need to set processing again? 
    // Actually handleScan sets isProcessing=false at end.

    if (state.isSaving) return; // Separate flag for save operation
    state.isSaving = true;

    try {
        elements.saveBtn.classList.add('loading');
        elements.saveBtn.textContent = 'Saving...';

        const payload = {
            student_id: state.currentStudentData.student_id,
            bus_number: state.currentStudentData.bus_number,
            scan_type: state.currentScanType,
            role: state.role, // Pass role
            auto_save: isAutoSave
        };

        const response = await fetch(`${CONFIG.API_BASE_URL}/attendance/save`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (!response.ok) {
            if (response.status === 400) {
                throw new Error(result.detail || 'Attendance already marked today');
            }
            if (response.status === 403) {
                throw new Error(result.detail || 'Scanning outside allowed hours');
            }
            throw new Error(result.detail || 'Failed to save attendance');
        }

        // Save success logic
        const studentId = state.currentStudentData.student_id;
        state.lastScannedId = studentId;
        localStorage.setItem('lastScannedId', studentId);

        showStatus(
            'success',
            'Success!',
            `Attendance saved for ${studentId} at ${result.timestamp}`
        );

        setTimeout(() => {
            resetForm();
            loadTodayAttendance();
            elements.scanInput.focus();
        }, 1500);

    } catch (error) {
        console.error('✗ Save error:', error);
        showStatus('error', 'Save Failed', error.message);

        // Reset button
        elements.saveBtn.classList.remove('loading');
        elements.saveBtn.innerHTML = `Save Attendance`;
    } finally {
        state.isSaving = false;
    }
}

/**
 * Reset form
 */
function resetForm() {
    state.currentStudentData = null;
    state.isSaving = false;

    elements.previewSection.style.display = 'none';
    elements.statusSection.style.display = 'none';
    elements.scanInput.value = '';
    elements.busNumberInput.value = '';

    elements.saveBtn.classList.remove('loading');
    elements.saveBtn.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M16 6L8 14L4 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Save Attendance
    `;

    elements.scanInput.focus();

    // If we were in scan mode, restart the camera automatically for the next person
    if (state.lastUsedMode === 'camera') {
        startCamera();
    }
}

/**
 * Show status message
 */
function showStatus(type, title, description) {
    elements.statusTitle.textContent = title;
    elements.statusDescription.textContent = description;
    elements.statusMessage.className = 'status-message ' + type;

    // Icons
    const icons = {
        success: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M20 6L9 17L4 12" stroke="white" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
        error: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M18 6L6 18M6 6L18 18" stroke="white" stroke-width="3" stroke-linecap="round"/></svg>`,
        warning: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><path d="M12 8V12M12 16H12.01M21 12C21 16.97 16.97 21 12 21C7.03 21 3 16.97 3 12C3 7.03 7.03 3 12 3C16.97 3 21 7.03 21 12Z" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>`,
        info: `<svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="white" stroke-width="2"/><path d="M12 8V12M12 16H12.01" stroke="white" stroke-width="2" stroke-linecap="round"/></svg>`,
    };
    elements.statusIcon.innerHTML = icons[type] || icons.info;

    elements.statusSection.style.display = 'block';
    elements.statusSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    if (type !== 'error') {
        setTimeout(() => {
            elements.statusSection.style.display = 'none';
        }, CONFIG.AUTO_CLEAR_TIMEOUT);
    }
}

/**
 * Load today's attendance
 * Updated to support Role-Based Visibility
 */
async function loadTodayAttendance() {
    try {
        let url = `${CONFIG.API_BASE_URL}/attendance/today?role=${state.role}`;

        // If student, we need a student_id to show THEIR attendance.
        // But since we don't have login, we can't persistent know "who" the student is until they scan.
        // User rule: "Students can view only today’s attendance status."
        // We likely can't show a LIST for students. We just show "No records (scan to check)" or similar.
        // Only if we just scanned successfully can we show that record? 
        // For now, if role is student, we might just not load the list to preserve privacy, 
        // or passing a dummy ID/empty might return empty list.

        // Actually, if role is student, let's NOT fetch list unless we just scanned?
        // But the requirement says "Students can view only today’s attendance status".
        // I will implement: Admin -> Fetches all. Student -> Fetches nothing initially (empty), 
        // until they scan, but usually the list is "Today's Attendance".
        // Let's just fetch. The backend filters: if student & no ID -> returns error or empty.

        // Let's modify: If student, don't auto-load list on init.
        const studentIdToFetch = state.lastScannedId || (state.currentStudentData ? state.currentStudentData.student_id : null);

        if (state.role === 'student' && !studentIdToFetch) {
            elements.attendanceTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-state">Scan your ID to mark attendance</td>
                </tr>
            `;
            elements.todayCount.textContent = '-';
            return;
        }

        if (state.role === 'student' && studentIdToFetch) {
            url += `&student_id=${studentIdToFetch}`;
        }

        const response = await fetch(url);
        if (!response.ok) {
            // Can happen if student_id missing
            return;
        }

        const data = await response.json();
        elements.todayCount.textContent = data.total_present;

        if (data.attendance_list && data.attendance_list.length > 0) {
            const rows = data.attendance_list.map(record => `
                <tr>
                    <td data-label="Student ID">${record.student_id}</td>
                    <td data-label="Bus Number"><span class="bus-badge">${record.bus_number}</span></td>
                    <td data-label="Time">${record.scan_time}</td>
                    <td data-label="Type">${capitalizeFirst(record.scan_type)}</td>
                </tr>
            `).join('');
            elements.attendanceTableBody.innerHTML = rows;
        } else {
            elements.attendanceTableBody.innerHTML = `
                <tr>
                    <td colspan="4" class="empty-state">No attendance records found</td>
                </tr>
            `;
        }

    } catch (error) {
        console.error('List load error', error);
    }
}

// =====================================================
// Core Functions
// =====================================================
/**
 * Check system health
 */
async function checkSystemHealth() {
    try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
            const health = await response.json();
            if (health.status === 'healthy') {
                updateSystemStatus('Ready', 'success');
            } else {
                updateSystemStatus('Database Error', 'error');
            }
        } else {
            updateSystemStatus('Backend Offline', 'error');
        }
    } catch (error) {
        updateSystemStatus('Offline', 'error');
    }
}

function updateSystemStatus(text, type) {
    const badge = elements.systemStatus;
    const dot = badge.querySelector('.status-dot');
    badge.textContent = '';
    badge.appendChild(dot);
    badge.appendChild(document.createTextNode(text));

    if (type === 'success') {
        badge.style.background = 'rgba(22, 163, 74, 0.1)';
        badge.style.borderColor = 'var(--success-color)';
        badge.style.color = 'var(--success-color)';
        dot.style.background = 'var(--success-color)';
    } else {
        badge.style.background = 'rgba(220, 38, 38, 0.1)';
        badge.style.borderColor = 'var(--error-color)';
        badge.style.color = 'var(--error-color)';
        dot.style.background = 'var(--error-color)';
    }
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Check time every minute to auto-update UI
setInterval(checkTimeWindow, 60000);

// Auto-refresh
setInterval(() => {
    // Only auto-refresh if Admin
    if (state.role === 'admin') {
        loadTodayAttendance();
    }
}, 30000);

/**
 * Registration Modal Functions
 */
function showRegisterModal(studentId, busNumber) {
    elements.regStudentId.value = studentId;
    elements.regRollNumber.value = studentId;
    elements.regBusNumber.value = busNumber;
    elements.regStudentName.value = '';
    elements.registerModal.style.display = 'flex';
    elements.regStudentName.focus();
}

function closeRegisterModal() {
    elements.registerModal.style.display = 'none';
    elements.scanInput.value = '';
    elements.scanInput.focus();
}

async function submitStudentRegistration(e) {
    e.preventDefault();
    const payload = {
        student_id: elements.regStudentId.value.trim().toUpperCase(),
        name: elements.regStudentName.value.trim(),
        roll_number: elements.regRollNumber.value.trim().toUpperCase(),
        bus_number: elements.regBusNumber.value.trim().toUpperCase()
    };
    
    try {
        showStatus('info', 'Registering...', 'Saving new student record');
        
        const response = await fetch(`${CONFIG.API_BASE_URL}/student/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.detail || 'Failed to register student');
        }
        
        closeRegisterModal();
        
        // Auto-save attendance for newly registered student
        state.currentStudentData = {
            student_id: payload.student_id,
            bus_number: payload.bus_number
        };
        await saveAttendance();
        
    } catch (error) {
        console.error('✗ Registration error:', error);
        showStatus('error', 'Registration Failed', error.message);
    }
}
