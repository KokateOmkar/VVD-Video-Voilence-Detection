from flask import Flask, request, jsonify, render_template
from pathlib import Path
from models.violence_detection_model import FightDetectionModel

app = Flask(__name__)

# Define the relative path to the model weights
model_path = Path('fight_detection_yolov8/Yolo_nano_weights.pt')
# Initialize the FightDetectionModel
model = FightDetectionModel(model_path)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'video' not in request.files:
        return jsonify({'error': 'No file uploaded.'}), 400

    video_file = request.files['video']
    video_path = Path('uploads') / video_file.filename
    video_file.save(video_path)

    # Run the detection model on the uploaded video
    results = model.detect(video_path)

    # Process results if needed and prepare a response
    # For now, we'll just return the results object as JSON
    return jsonify({'message': 'Video processed successfully.', 'results': results}), 
