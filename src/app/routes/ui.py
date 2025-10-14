"""Web UI endpoint."""
from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["ui"])


def _render_ui() -> str:
    """Return the built-in web interface for the face recognition system."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Face Recognition System</title>
        <style>
            :root {
                --bg: #050b18;
                --glass: rgba(15, 23, 42, 0.78);
                --glass-soft: rgba(15, 23, 42, 0.55);
                --border: rgba(100, 116, 139, 0.28);
                --accent: #38bdf8;
                --accent-strong: #22d3ee;
                --accent-contrast: #020617;
                --text-primary: #e2e8f0;
                --text-secondary: #94a3b8;
                --success: #34d399;
                --warning: #facc15;
                --error: #f87171;
                --radius-lg: 22px;
                --radius-md: 16px;
                --shadow-soft: 0 20px 60px rgba(2, 6, 23, 0.55);
            }
            *, *::before, *::after {
                box-sizing: border-box;
            }
            body {
                margin: 0;
                min-height: 100vh;
                background: radial-gradient(circle at 18% 20%, rgba(59, 130, 246, 0.26), transparent 58%),
                            radial-gradient(circle at 82% 8%, rgba(14, 165, 233, 0.22), transparent 55%),
                            var(--bg);
                font-family: "Inter", "Segoe UI", sans-serif;
                color: var(--text-primary);
            }
            h1 {
                font-size: clamp(32px, 4vw, 48px);
                font-weight: 700;
                margin: 0 0 8px;
            }
            h3 {
                font-size: 22px;
                font-weight: 600;
                margin: 0;
            }
            p {
                margin: 0;
                color: var(--text-secondary);
            }
            .container {
                width: min(1180px, 92%);
                margin: 0 auto;
                padding: 80px 0 120px;
                display: flex;
                flex-direction: column;
                gap: 36px;
            }
            .hero-card {
                background: linear-gradient(140deg, rgba(15, 23, 42, 0.88), rgba(8, 47, 73, 0.78));
                border-radius: var(--radius-lg);
                padding: 42px;
                border: 1px solid rgba(148, 163, 184, 0.16);
                box-shadow: var(--shadow-soft);
                display: flex;
                flex-wrap: wrap;
                gap: 28px;
                justify-content: space-between;
                backdrop-filter: blur(20px);
            }
            .hero-copy {
                max-width: 520px;
            }
            .hero-copy p {
                font-size: 16px;
                line-height: 1.6;
            }
            .tag-group {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-top: 12px;
            }
            .tag {
                padding: 6px 14px;
                border-radius: 999px;
                font-size: 12px;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                background: rgba(148, 163, 184, 0.14);
                color: var(--text-secondary);
            }
            .tag.live {
                color: #fca5a5;
                background: rgba(248, 113, 113, 0.12);
                border: 1px solid rgba(248, 113, 113, 0.32);
                position: relative;
                padding-left: 28px;
            }
            .tag.live::before {
                content: "";
                position: absolute;
                left: 12px;
                top: 50%;
                transform: translateY(-50%);
                width: 10px;
                height: 10px;
                border-radius: 50%;
                background: #f87171;
                box-shadow: 0 0 0 6px rgba(248, 113, 113, 0.22);
            }
            .metrics-strip {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 16px;
                min-width: 260px;
            }
            .metric-card {
                background: rgba(15, 23, 42, 0.6);
                border-radius: var(--radius-md);
                padding: 18px;
                border: 1px solid rgba(148, 163, 184, 0.12);
                text-align: left;
            }
            .metric-card span {
                display: block;
            }
            .metric-label {
                text-transform: uppercase;
                font-size: 12px;
                letter-spacing: 0.08em;
                color: rgba(148, 163, 184, 0.8);
            }
            .metric-value {
                margin-top: 8px;
                font-size: 26px;
                font-weight: 700;
                color: var(--accent);
            }
            .section {
                background: var(--glass);
                border-radius: var(--radius-lg);
                padding: 30px;
                border: 1px solid var(--border);
                box-shadow: var(--shadow-soft);
                backdrop-filter: blur(18px);
                display: flex;
                flex-direction: column;
                gap: 24px;
            }
            .section-header {
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: center;
                gap: 16px;
            }
            .section-header h3 {
                margin-bottom: 6px;
            }
            .actions {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: flex-end;
            }
            .info-block {
                background: rgba(148, 163, 184, 0.08);
                border-radius: var(--radius-md);
                padding: 18px;
                border: 1px solid rgba(148, 163, 184, 0.16);
                min-height: 84px;
                color: var(--text-secondary);
            }
            button {
                appearance: none;
                border: none;
                padding: 11px 20px;
                border-radius: 999px;
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                transition: transform 0.18s ease, box-shadow 0.18s ease;
                background: linear-gradient(135deg, var(--accent) 0%, var(--accent-strong) 100%);
                color: var(--accent-contrast);
                box-shadow: 0 14px 30px rgba(34, 211, 238, 0.25);
            }
            button:hover {
                transform: translateY(-1px);
                box-shadow: 0 18px 36px rgba(34, 211, 238, 0.32);
            }
            button:active {
                transform: translateY(0);
                box-shadow: 0 12px 24px rgba(34, 211, 238, 0.24);
            }
            button.secondary {
                background: rgba(148, 163, 184, 0.16);
                color: var(--text-primary);
                box-shadow: none;
            }
            button.secondary:hover {
                box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.35);
            }
            input {
                padding: 12px 16px;
                border-radius: var(--radius-md);
                border: 1px solid rgba(148, 163, 184, 0.2);
                background: rgba(15, 23, 42, 0.55);
                color: var(--text-primary);
                font-size: 14px;
                width: 100%;
                transition: border 0.2s ease, box-shadow 0.2s ease;
            }
            input[type="file"] {
                padding: 12px;
            }
            input:focus {
                outline: none;
                border-color: rgba(34, 211, 238, 0.65);
                box-shadow: 0 0 0 3px rgba(34, 211, 238, 0.18);
            }
            .webcam-section {
                align-items: center;
                text-align: center;
            }
            .video-wall {
                display: grid;
                gap: 18px;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                width: 100%;
            }
            .video-frame {
                position: relative;
                background: #000;
                border-radius: 20px;
                padding: 14px;
                border: 1px solid rgba(148, 163, 184, 0.2);
                box-shadow: inset 0 0 0 1px rgba(56, 189, 248, 0.08);
            }
            .video-frame::after {
                content: "";
                position: absolute;
                inset: 8px;
                border-radius: 14px;
                border: 1px solid rgba(56, 189, 248, 0.12);
                pointer-events: none;
            }
            video, canvas {
                width: 100%;
                aspect-ratio: 16 / 9;
                border-radius: 14px;
                background: #000;
                border: none;
                display: block;
            }
            #canvas {
                box-shadow: inset 0 0 0 1px rgba(56, 189, 248, 0.22);
            }
            .control-row {
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                justify-content: center;
            }
            .guidance {
                font-size: 18px;
                font-weight: 600;
                padding: 16px 20px;
                border-radius: var(--radius-md);
                margin: 0;
                background: rgba(148, 163, 184, 0.12);
                color: var(--text-primary);
            }
            .guidance.success { color: var(--success); }
            .guidance.warning { color: var(--warning); }
            .guidance.error { color: var(--error); }
            .progress-bar {
                width: 100%;
                height: 16px;
                background: rgba(15, 23, 42, 0.65);
                border-radius: 999px;
                overflow: hidden;
                border: 1px solid rgba(148, 163, 184, 0.18);
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(135deg, var(--accent) 0%, #6366f1 100%);
                border-radius: inherit;
                transition: width 0.35s ease;
            }
            .result {
                margin: 0;
                padding: 16px 18px;
                border-radius: var(--radius-md);
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(148, 163, 184, 0.2);
                color: var(--text-secondary);
            }
            .success {
                background: rgba(52, 211, 153, 0.12);
                color: var(--success);
                border-color: rgba(52, 211, 153, 0.32);
            }
            .error {
                background: rgba(248, 113, 113, 0.12);
                color: var(--error);
                border-color: rgba(248, 113, 113, 0.32);
            }
            .warning {
                background: rgba(250, 204, 21, 0.12);
                color: var(--warning);
                border-color: rgba(250, 204, 21, 0.28);
            }
            .info {
                background: rgba(56, 189, 248, 0.12);
                color: var(--accent);
                border-color: rgba(56, 189, 248, 0.28);
            }
            .modal {
                position: fixed;
                z-index: 1000;
                inset: 0;
                display: flex;
                align-items: center;
                justify-content: center;
                background: rgba(2, 6, 23, 0.72);
                backdrop-filter: blur(12px);
            }
            .modal-content {
                width: min(960px, 92%);
                max-height: 80vh;
                overflow-y: auto;
                background: var(--glass);
                border-radius: var(--radius-lg);
                border: 1px solid var(--border);
                padding: 28px;
                box-shadow: var(--shadow-soft);
            }
            .close {
                font-size: 28px;
                color: var(--text-secondary);
                float: right;
                cursor: pointer;
            }
            .close:hover {
                color: var(--text-primary);
            }
            .analytics-grid {
                display: grid;
                gap: 20px;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                margin: 24px 0;
            }
            .analytics-card {
                background: rgba(15, 23, 42, 0.62);
                border-radius: var(--radius-md);
                padding: 20px;
                border: 1px solid rgba(148, 163, 184, 0.16);
            }
            .analytics-card .metric {
                font-size: 28px;
                font-weight: 700;
                color: var(--accent);
            }
            @media (max-width: 768px) {
                .hero-card {
                    padding: 32px;
                }
                .section {
                    padding: 24px;
                }
                .control-row {
                    justify-content: stretch;
                }
                .control-row button {
                    flex: 1 1 45%;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero-card">
                <div class="hero-copy">
                    <div class="tag live">Live</div>
                    <h1>Face Recognition System v2.0</h1>
                    <p>Monitor real-time attendance, enroll students effortlessly, and gain insight from detailed analytics&mdash;all within a cinematic control room interface.</p>
                    <div class="tag-group">
                        <span class="tag">High Fidelity Stream</span>
                        <span class="tag">Guided Enrollment</span>
                        <span class="tag">FAISS Acceleration</span>
                    </div>
                </div>
                <div class="metrics-strip">
                    <div class="metric-card">
                        <span class="metric-label">Enrolled Faces</span>
                        <span class="metric-value" id="metricEnrolled">--</span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-label">Today&rsquo;s Attendance</span>
                        <span class="metric-value" id="metricToday">--</span>
                    </div>
                    <div class="metric-card">
                        <span class="metric-label">Last Recognition</span>
                        <span class="metric-value" id="metricLast">--</span>
                    </div>
                </div>
            </div>
            <div class="section">
                <div class="section-header">
                    <div>
                        <h3>System Status Console</h3>
                        <p>Live system metrics, attendance summaries, and export utilities.</p>
                    </div>
                    <div class="actions">
                        <button class="secondary" onclick="getStatus()">Refresh Status</button>
                        <button class="secondary" onclick="getAttendance()">View Today&rsquo;s Attendance</button>
                        <button onclick="showAnalytics()">📊 Analytics Dashboard</button>
                        <button onclick="exportReport()">📄 Export Report</button>
                    </div>
                </div>
                <div class="info-block" id="status"></div>
                <div class="info-block" id="attendance"></div>
            </div>
            <div class="section webcam-section">
                <div class="section-header">
                    <div>
                        <h3>Live Recognition Feed</h3>
                        <p>Monitor camera feed, enroll new faces, and track recognition overlays.</p>
                    </div>
                </div>
                <div class="video-wall">
                    <div class="video-frame">
                        <video id="video" width="400" height="300" autoplay muted></video>
                    </div>
                    <div class="video-frame">
                        <canvas id="canvas" width="400" height="300"></canvas>
                    </div>
                </div>
                <div class="control-row">
                    <input type="text" id="enrollName" placeholder="Enter name to enroll">
                    <button onclick="enrollFromWebcam()">Quick Enroll (1 Photo)</button>
                    <button onclick="enrollGuidedFromWebcam()">Guided Enroll (15 Photos - Best Accuracy)</button>
                    <button onclick="startRecognition()">Start Recognition</button>
                    <button class="secondary" onclick="stopRecognition()">Stop Recognition</button>
                </div>
                <div id="enrollmentProgress" style="display: none;">
                    <div class="progress-bar">
                        <div id="progressFill" class="progress-fill" style="width: 0%;"></div>
                    </div>
                    <p id="guidanceText" class="guidance info">Get ready...</p>
                </div>
                <div id="webcamResult"></div>
            </div>
            <div class="section">
                <div class="section-header">
                    <div>
                        <h3>Upload & Offline Recognition</h3>
                        <p>Process stored images for enrollment or recognition results.</p>
                    </div>
                </div>
                <div class="control-row">
                    <input type="file" id="imageFile" accept="image/*" multiple>
                    <input type="text" id="uploadName" placeholder="Name (for enrollment)">
                    <button onclick="enrollFromFile()">Enroll from Files</button>
                    <button class="secondary" onclick="recognizeFromFile()">Recognize from File</button>
                </div>
                <div id="uploadResult" class="info-block"></div>
            </div>
            <div id="analyticsModal" class="modal" style="display: none;">
                <div class="modal-content">
                    <span class="close" onclick="closeAnalytics()">&times;</span>
                    <h2>📊 Analytics Dashboard</h2>
                    <div id="analyticsContent">Loading...</div>
                </div>
            </div>
        </div>
        <script>
            const API_BASE = '/api';
            let video, canvas, ctx;
            let recognitionInterval;
            async function initWebcam() {
                video = document.getElementById('video');
                canvas = document.getElementById('canvas');
                ctx = canvas.getContext('2d');
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                } catch (err) {
                    document.getElementById('webcamResult').innerHTML = '<div class="error">Camera access denied</div>';
                }
            }
            function updateHeroMetrics(data) {
                const enrolled = document.getElementById('metricEnrolled');
                const today = document.getElementById('metricToday');
                const last = document.getElementById('metricLast');
                if (enrolled) {
                    enrolled.textContent = data.enrolled_count ?? '--';
                }
                if (today) {
                    today.textContent = data.attendance?.today_attendance ?? '--';
                }
                if (last) {
                    const recentName = data.attendance?.today_names?.slice(-1)[0];
                    last.textContent = recentName ? recentName : 'Idle';
                }
            }
            async function getStatus() {
                try {
                    const response = await fetch(`${API_BASE}/status`);
                    const data = await response.json();
                    document.getElementById('status').innerHTML = `
                        <div class="success">
                            <strong>Enrolled:</strong> ${data.enrolled_count} faces<br>
                            <strong>Names:</strong> ${data.enrolled_names.join(', ') || 'None'}<br>
                            <strong>Model:</strong> ${data.model}<br>
                            <strong>Today's Attendance:</strong> ${data.attendance.today_attendance} people
                        </div>
                    `;
                    updateHeroMetrics(data);
                } catch (err) {
                    document.getElementById('status').innerHTML = '<div class="error">Failed to get status</div>';
                }
            }
            async function getAttendance() {
                try {
                    const response = await fetch(`${API_BASE}/attendance`);
                    const data = await response.json();
                    document.getElementById('attendance').innerHTML = `
                        <div class="info">
                            <h4>📊 Attendance Statistics</h4>
                            <strong>Today (${new Date().toLocaleDateString()}):</strong> ${data.today_attendance} people<br>
                            <strong>Present Today:</strong> ${data.today_names.join(', ') || 'None'}<br>
                            <strong>Total Days Recorded:</strong> ${data.total_days_recorded}<br>
                            <strong>Total Records:</strong> ${data.total_attendance_records}
                        </div>
                    `;
                    updateHeroMetrics({
                        enrolled_count: document.getElementById('metricEnrolled')?.textContent,
                        attendance: data
                    });
                } catch (err) {
                    document.getElementById('attendance').innerHTML = '<div class="error">Failed to get attendance</div>';
                }
            }
            function captureFrame() {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                return new Promise(resolve => {
                    canvas.toBlob(resolve, 'image/jpeg', 0.9);
                });
            }
            async function enrollFromWebcam() {
                const name = document.getElementById('enrollName').value.trim();
                if (!name) {
                    alert('Please enter a name');
                    return;
                }
                const blob = await captureFrame();
                const formData = new FormData();
                formData.append('name', name);
                formData.append('files', blob, 'webcam.jpg');
                try {
                    const response = await fetch(`${API_BASE}/enroll`, { method: 'POST', body: formData });
                    const data = await response.json();
                    if (response.ok) {
                        document.getElementById('webcamResult').innerHTML = `<div class="success">${data.message}</div>`;
                        getStatus();
                    } else {
                        document.getElementById('webcamResult').innerHTML = `<div class="error">${data.detail}</div>`;
                    }
                } catch (err) {
                    document.getElementById('webcamResult').innerHTML = '<div class="error">Enrollment failed</div>';
                }
            }
            async function enrollGuidedFromWebcam() {
                const name = document.getElementById('enrollName').value.trim();
                if (!name) {
                    alert('Please enter a name');
                    return;
                }
                const progressDiv = document.getElementById('enrollmentProgress');
                const progressFill = document.getElementById('progressFill');
                const guidanceText = document.getElementById('guidanceText');
                const resultDiv = document.getElementById('webcamResult');
                progressDiv.style.display = 'block';
                resultDiv.innerHTML = '';
                const formData = new FormData();
                formData.append('name', name);
                const poses = [
                    { instruction: "Look straight at the camera", duration: 2000, count: 3 },
                    { instruction: "Turn your head slightly LEFT", duration: 1500, count: 2 },
                    { instruction: "Turn your head slightly RIGHT", duration: 1500, count: 2 },
                    { instruction: "Look straight again", duration: 1500, count: 2 },
                    { instruction: "Tilt your head slightly UP", duration: 1500, count: 2 },
                    { instruction: "Tilt your head slightly DOWN", duration: 1500, count: 2 },
                    { instruction: "Look straight - final shots", duration: 2000, count: 2 }
                ];
                let totalPhotos = 0;
                const targetPhotos = 15;
                try {
                    for (const pose of poses) {
                        guidanceText.innerHTML = `${pose.instruction}`;
                        guidanceText.className = 'guidance info';
                        await new Promise(resolve => setTimeout(resolve, 800));
                        for (let i = 0; i < pose.count; i++) {
                            for (let countdown = 3; countdown > 0; countdown--) {
                                guidanceText.innerHTML = `${pose.instruction}<br>📸 ${countdown}...`;
                                await new Promise(resolve => setTimeout(resolve, 300));
                            }
                            guidanceText.innerHTML = `${pose.instruction}<br>📸 CLICK!`;
                            guidanceText.className = 'guidance success';
                            const blob = await captureFrame();
                            formData.append('files', blob, `guided_${totalPhotos}.jpg`);
                            totalPhotos++;
                            const progress = (totalPhotos / targetPhotos) * 100;
                            progressFill.style.width = `${progress}%`;
                            await new Promise(resolve => setTimeout(resolve, 500));
                            if (i < pose.count - 1) {
                                guidanceText.innerHTML = `${pose.instruction}<br>Hold position...`;
                                guidanceText.className = 'guidance warning';
                                await new Promise(resolve => setTimeout(resolve, 800));
                            }
                        }
                    }
                    guidanceText.innerHTML = '🔄 Processing your enrollment...';
                    guidanceText.className = 'guidance info';
                    const response = await fetch(`${API_BASE}/enroll`, { method: 'POST', body: formData });
                    const data = await response.json();
                    if (response.ok) {
                        guidanceText.innerHTML = '✅ Enrollment Complete!';
                        guidanceText.className = 'guidance success';
                        resultDiv.innerHTML = `<div class="success">
                                <strong>${data.message}</strong><br>
                                📊 Quality Score: ${(data.avg_quality * 100).toFixed(1)}%<br>
                                📸 Photos Used: ${data.successful_enrollments}/${totalPhotos}<br>
                                🎯 Total Embeddings: ${data.total_embeddings}
                            </div>`;
                        getStatus();
                    } else {
                        throw new Error(data.detail);
                    }
                } catch (err) {
                    guidanceText.innerHTML = '❌ Enrollment Failed';
                    guidanceText.className = 'guidance error';
                    resultDiv.innerHTML = `<div class="error">${err.message || 'Enrollment failed'}</div>`;
                }
                setTimeout(() => {
                    progressDiv.style.display = 'none';
                }, 3000);
            }
            async function startRecognition() {
                if (recognitionInterval) return;
                recognitionInterval = setInterval(async () => {
                    const blob = await captureFrame();
                    const formData = new FormData();
                    formData.append('file', blob, 'webcam.jpg');
                    try {
                        const response = await fetch(`${API_BASE}/recognize?threshold=0.5`, {
                            method: 'POST',
                            body: formData,
                        });
                        const data = await response.json();
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        let resultText = `Faces: ${data.count}`;
                        let attendanceText = '';
                        if (data.attendance_logged && data.attendance_logged.length > 0) {
                            attendanceText = `<br>✅ Attendance logged: ${data.attendance_logged.join(', ')}`;
                        }
                        data.faces.forEach(face => {
                            const [x1, y1, x2, y2] = face.bbox;
                            ctx.strokeStyle = face.matched ? '#00ff00' : '#ff0000';
                            ctx.lineWidth = 3;
                            ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);
                            const label = face.matched ?
                                `${face.name} (${(face.confidence * 100).toFixed(0)}%)` :
                                `Unknown (${(face.confidence * 100).toFixed(0)}%)`;
                            ctx.font = '16px Arial';
                            const textMetrics = ctx.measureText(label);
                            const textWidth = textMetrics.width;
                            ctx.fillStyle = 'rgba(0,0,0,0.8)';
                            ctx.fillRect(x1, y1 - 30, textWidth + 12, 30);
                            ctx.fillStyle = face.matched ? '#00ff00' : '#ff0000';
                            ctx.fillText(label, x1 + 6, y1 - 8);
                            if (face.matched) {
                                resultText += ` | ${face.name}: ${(face.confidence * 100).toFixed(0)}%`;
                            }
                        });
                        document.getElementById('webcamResult').innerHTML = `<div class="result">${resultText}${attendanceText}</div>`;
                    } catch (err) {
                        console.error('Recognition error:', err);
                    }
                }, 1000);
            }
            function stopRecognition() {
                if (recognitionInterval) {
                    clearInterval(recognitionInterval);
                    recognitionInterval = null;
                }
            }
            async function enrollFromFile() {
                const fileInput = document.getElementById('imageFile');
                const name = document.getElementById('uploadName').value.trim();
                if (!fileInput.files.length) {
                    alert('Please select at least one image');
                    return;
                }
                if (!name) {
                    alert('Please enter a name');
                    return;
                }
                const formData = new FormData();
                formData.append('name', name);
                for (const file of fileInput.files) {
                    formData.append('files', file);
                }
                try {
                    const response = await fetch(`${API_BASE}/enroll`, { method: 'POST', body: formData });
                    const data = await response.json();
                    if (response.ok) {
                        let message = data.message;
                        if (data.avg_quality) {
                            message += `<br>Quality Score: ${data.avg_quality}`;
                        }
                        document.getElementById('uploadResult').innerHTML = `<div class="success">${message}</div>`;
                        getStatus();
                    } else {
                        document.getElementById('uploadResult').innerHTML = `<div class="error">${data.detail}</div>`;
                    }
                } catch (err) {
                    document.getElementById('uploadResult').innerHTML = '<div class="error">Enrollment failed</div>';
                }
            }
            async function recognizeFromFile() {
                const fileInput = document.getElementById('imageFile');
                if (!fileInput.files[0]) {
                    alert('Please select an image');
                    return;
                }
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                try {
                    const response = await fetch(`${API_BASE}/recognize?threshold=0.5`, {
                        method: 'POST',
                        body: formData,
                    });
                    const data = await response.json();
                    let resultHtml = `<div class="result">Found ${data.count} faces:<br>`;
                    data.faces.forEach(face => {
                        const status = face.matched ?
                            `<span style="color: green;">✓ ${face.name} (${face.confidence.toFixed(2)})</span>` :
                            `<span style="color: red;">✗ Unknown (${face.confidence.toFixed(2)})</span>`;
                        resultHtml += `${status}<br>`;
                    });
                    resultHtml += '</div>';
                    document.getElementById('uploadResult').innerHTML = resultHtml;
                } catch (err) {
                }
            }
            async function showAnalytics() {
                document.getElementById('analyticsModal').style.display = 'block';
                document.getElementById('analyticsContent').innerHTML = 'Loading analytics...';
                try {
                    const response = await fetch(`${API_BASE}/analytics/dashboard`);
                    const data = await response.json();
                    if (data.error) {
                        document.getElementById('analyticsContent').innerHTML = `<div class="error">${data.error}</div>`;
                        return;
                    }
                    const html = `
                        <div class="analytics-grid">
                            <div class="analytics-card">
                                <h4>📊 Daily Statistics</h4>
                                <div class="metric">${data.daily_stats?.avg_daily_attendance?.toFixed(1) || 0}</div>
                                <p>Average Daily Attendance</p>
                                <p>Max: ${data.daily_stats?.max_daily_attendance || 0} people</p>
                            </div>
                            <div class="analytics-card">
                                <h4>🎯 System Health</h4>
                                <div class="metric">${data.system_health?.database_health?.enrolled_people || 0}</div>
                                <p>Enrolled People</p>
                                <p>Embeddings: ${data.system_health?.database_health?.total_embeddings || 0}</p>
                            </div>
                            <div class="analytics-card">
                                <h4>📈 Confidence Analysis</h4>
                                <div class="metric">${(data.confidence_analysis?.overall_stats?.mean * 100)?.toFixed(1) || 0}%</div>
                                <p>Average Confidence</p>
                                <p>Records: ${data.confidence_analysis?.overall_stats?.count || 0}</p>
                            </div>
                            <div class="analytics-card">
                                <h4>⏰ Recent Activity</h4>
                                <div class="metric">${data.system_health?.recent_activity?.last_24h_recognitions || 0}</div>
                                <p>Recognitions (24h)</p>
                                <p>Unique: ${data.system_health?.recent_activity?.unique_people_24h || 0}</p>
                            </div>
                        </div>
                        <div class="analytics-card">
                            <h4>👥 Person Statistics</h4>
                            <div style="max-height: 200px; overflow-y: auto;">
                                ${Object.entries(data.person_stats || {}).map(([name, stats]) => `
                                    <p><strong>${name}:</strong> ${stats.Date_nunique} days, 
                                    ${(stats.attendance_rate || 0).toFixed(1)}% attendance rate</p>
                                `).join('')}
                            </div>
                        </div>
                    `;
                    document.getElementById('analyticsContent').innerHTML = html;
                } catch (error) {
                    document.getElementById('analyticsContent').innerHTML = `<div class="error">Failed to load analytics: ${error.message}</div>`;
                }
            }
            function closeAnalytics() {
                document.getElementById('analyticsModal').style.display = 'none';
            }
            async function exportReport() {
                try {
                    const response = await fetch(`${API_BASE}/analytics/export?format=json`);
                    const data = await response.json();
                    if (data.error) {
                        alert('Export failed: ' + data.error);
                    } else {
                        alert('Report exported successfully to: ' + data.file_path);
                    }
                } catch (error) {
                    alert('Export failed: ' + error.message);
                }
            }
            window.onload = initWebcam;
        </script>
    </body>
    </html>
    """


@router.get("/", response_class=HTMLResponse)
def get_root_ui() -> str:
    """Serve the UI at the application root."""
    return _render_ui()


@router.get("/ui", response_class=HTMLResponse)
def get_legacy_ui() -> str:
    """Retain legacy /ui path for backwards compatibility."""
    return _render_ui()
