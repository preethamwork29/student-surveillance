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
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
            .section { margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }
            input, button { padding: 10px; margin: 5px; font-size: 14px; }
            button { background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .result { margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
            .warning { background: #fff3cd; color: #856404; }
            .info { background: #d1ecf1; color: #0c5460; }
            video, canvas { border: 2px solid #333; border-radius: 8px; margin: 10px; }
            .webcam-section { text-align: center; }
            .guidance { font-size: 18px; font-weight: bold; padding: 15px; margin: 10px 0; border-radius: 8px; }
            .progress-bar { width: 100%; height: 20px; background: #e9ecef; border-radius: 10px; margin: 10px 0; }
            .progress-fill { height: 100%; background: #007bff; border-radius: 10px; transition: width 0.3s; }
            .modal { position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.5); }
            .modal-content { background-color: #fefefe; margin: 5% auto; padding: 20px; border: 1px solid #888; width: 90%; max-width: 1000px; border-radius: 10px; max-height: 80vh; overflow-y: auto; }
            .close { color: #aaa; float: right; font-size: 28px; font-weight: bold; cursor: pointer; }
            .close:hover { color: black; }
            .analytics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
            .analytics-card { background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6; }
            .metric { font-size: 24px; font-weight: bold; color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Face Recognition System v2.0</h1>
            <div class="section">
                <h3>System Status</h3>
                <button onclick="getStatus()">Refresh Status</button>
                <button onclick="getAttendance()">View Today's Attendance</button>
                <button onclick="showAnalytics()">📊 Analytics Dashboard</button>
                <button onclick="exportReport()">📄 Export Report</button>
                <div id="status"></div>
                <div id="attendance"></div>
            </div>
            <div class="section webcam-section">
                <h3>Live Webcam Recognition</h3>
                <video id="video" width="400" height="300" autoplay muted></video>
                <canvas id="canvas" width="400" height="300"></canvas>
                <br>
                <input type="text" id="enrollName" placeholder="Enter name to enroll">
                <button onclick="enrollFromWebcam()">Quick Enroll (1 Photo)</button>
                <button onclick="enrollGuidedFromWebcam()">Guided Enroll (15 Photos - Best Accuracy)</button>
                <button onclick="startRecognition()">Start Recognition</button>
                <button onclick="stopRecognition()">Stop Recognition</button>
                <div id="enrollmentProgress" style="display: none;">
                    <div class="progress-bar">
                        <div id="progressFill" class="progress-fill" style="width: 0%;"></div>
                    </div>
                    <div id="guidanceText" class="guidance info">Get ready...</div>
                </div>
                <div id="webcamResult"></div>
            </div>
            <div class="section">
                <h3>Upload Images</h3>
                <input type="file" id="imageFile" accept="image/*" multiple>
                <input type="text" id="uploadName" placeholder="Name (for enrollment)">
                <br>
                <button onclick="enrollFromFile()">Enroll from Files</button>
                <button onclick="recognizeFromFile()">Recognize from File</button>
                <div id="uploadResult"></div>
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
