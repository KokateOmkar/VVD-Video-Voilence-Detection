// Generate a unique client ID (UUID)
function generateUUID() { // Public Domain/MIT
    var d = new Date().getTime(); // Timestamp
    var d2 = (performance && performance.now && (performance.now() * 1000)) || 0; // Time in microseconds since page-load or 0 if unsupported
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16; // random number between 0 and 16
        if (d > 0) {
            r = (d + r) % 16 | 0;
            d = Math.floor(d / 16);
        } else {
            r = (d2 + r) % 16 | 0;
            d2 = Math.floor(d2 / 16);
        }
        return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
}

const clientId = generateUUID();
const ws = new WebSocket(`ws://${window.location.host}/ws/${clientId}`); // Fix: WebSocket URL with template literals

ws.onopen = () => {
    console.log('WebSocket connection established.');
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.progress !== undefined) {
        updateProgressBar(data.progress);
    }
};

ws.onclose = () => {
    console.log('WebSocket connection closed.');
};

document.getElementById('uploadForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent the default form submission

    const videoFile = document.getElementById('videoFile').files[0];
    if (!videoFile) {
        alert('Please select a video file.');
        return;
    }

    const formData = new FormData();
    formData.append('video', videoFile);

    // Show progress bar
    document.getElementById('progressContainer').style.display = 'block';
    updateProgressBar(0);
    document.getElementById('result').innerHTML = '';
    document.getElementById('annotatedVideo').style.display = 'none';

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: {
                'client-id': clientId // Send the client ID in headers
            },
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            document.getElementById('result').innerHTML = `<p>Error: ${data.error}</p>`; // Fix: Use backticks for string interpolation
            document.getElementById('progressContainer').style.display = 'none';
        } else {
            const message = data.violenceDetected ? 'Violence Detected!' : 'No Violence Detected.';
            const violenceInfo = `Violence Percentage: ${data.violencePercentage}%`; // Fix: Proper string interpolation
            const framesInfo = `Frames Processed: ${data.framesProcessed}`; // Fix: Proper string interpolation
            const videoUrl = data.annotatedVideoUrl;
            document.getElementById('result').innerHTML = `<p>${message}</p><p>${violenceInfo}</p><p>${framesInfo}</p>`;
            document.getElementById('videoSource').src = videoUrl;
            document.getElementById('annotatedVideo').load();
            document.getElementById('annotatedVideo').style.display = 'block';
            document.getElementById('progressContainer').style.display = 'none';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('result').innerHTML = `<p>An error occurred while detecting violence.</p>`; // Fix: Use backticks for HTML string
        document.getElementById('progressContainer').style.display = 'none';
    }
});

function updateProgressBar(progress) {
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    progressFill.style.width = `${progress}%`; // Fix: Proper template literal
    progressText.innerText = `${progress}%`; // Fix: Proper template literal
}
