document.getElementById('upload-button').addEventListener('click', () => {
    const fileInput = document.getElementById('video-upload');
    const file = fileInput.files[0];
    if (!file) {
        alert('Please select a video file.');
        return;
    }

    const formData = new FormData();
    formData.append('video', file);

    fetch('http://localhost:5000/upload', {  // Backend URL
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const videoPlayer = document.getElementById('video-player');
        videoPlayer.src = URL.createObjectURL(file);
        videoPlayer.play();
        
        const results = document.getElementById('detection-results');
        results.innerText = data.violenceDetected ? 'Violence Detected!' : 'No Violence Detected.';
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
