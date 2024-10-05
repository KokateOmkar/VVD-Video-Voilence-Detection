from flask import Flask, request, jsonify
from flask_cors import CORS
from models.violence_detection_model import ViolenceDetector
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

detector = ViolenceDetector()

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided.'}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No selected file.'}), 400
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    file.save(filepath)

    # Process video for violence detection
    violence_detected = detector.detect_violence(filepath)

    # Optionally, save results to MongoDB here

    return jsonify({'violenceDetected': violence_detected})

if __name__ == '__main__':
    app.run(debug=True)
