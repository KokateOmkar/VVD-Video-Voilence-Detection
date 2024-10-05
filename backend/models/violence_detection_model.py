from ultralytics import YOLO
import cv2  # OpenCV for video processing

class FightDetectionModel:
    def __init__(self, model_path):
        # Load the YOLOv8 model from the specified path
        self.model = YOLO(model_path)

    def detect(self, video_path):
        # Load the video using OpenCV
        cap = cv2.VideoCapture(str(video_path))
        results = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform inference
            detections = self.model(frame)
            results.append(detections)

        cap.release()
        
        # Process results
        processed_results = []
        for detection in results:
            for det in detection:
                boxes = det.boxes.cpu().numpy().tolist()
                scores = det.conf.cpu().numpy().tolist()
                classes = det.cls.cpu().numpy().tolist()
                processed_results.append({
                    'boxes': boxes,
                    'scores': scores,
                    'classes': classes
                })

        return processed_results
