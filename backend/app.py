from flask import Flask, request, jsonify
from models.violence_detection_model import FightDetectionModel

app = Flask(__name__)

# Set the path to the YOLO model weights
model_path = r'C:\Users\HP\Desktop\AI\VD\fight_detection_yolov8\Yolo_nano_weights.pt'
model = FightDetectionModel(model_path)

@app.route('/detect', methods=['POST'])
def detect_violence():
    # Assuming you're sending a video file via POST request
    if 'video' not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    video_file = request.files['video']
    video_path = f"C:/Users/HP/Desktop/AI/VD/backend/{video_file.filename}"
    video_file.save(video_path)  # Save the video to the backend

    # Call the detect method from the model
    results = model.detect(video_path)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
