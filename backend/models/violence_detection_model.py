from ultralytics import YOLO
import cv2  # OpenCV for video processing
import os

class FightDetectionModel:
    def __init__(self, model_path):
        # Load the YOLOv8 model from the specified path
        self.model = YOLO(model_path)
        # Define the class IDs that correspond to 'violence' or 'fight'
        # Adjust this based on your model's class labels
        self.violence_class_ids = [0]  # Example: '0' corresponds to 'fight'

    def detect(self, video_path, output_path, websocket=None):
        """
        Detect violence in the given video, annotate it, and save the annotated video.

        Args:
            video_path (str): Path to the input video.
            output_path (str): Path to save the annotated video.
            websocket (WebSocket, optional): WebSocket connection for progress updates.

        Returns:
            dict: Contains whether violence was detected, the percentage of frames with violence,
                  the number of frames processed, and the annotated video filename.
        """
        # Load the video using OpenCV
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise IOError(f"Cannot open video file {video_path}")

        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Ensure compatibility with MP4

        # Initialize video writer for the annotated video
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        violence_detected_frames = 0
        frames_processed = 0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Perform inference on the current frame
            results = self.model(frame)[0]  # Get the first result

            # Process detection results
            frame_violence = False
            for detection in results.boxes:
                cls = int(detection.cls.cpu().numpy())
                conf = float(detection.conf.cpu().numpy())
                if cls in self.violence_class_ids and conf > 0.5:
                    violence_detected_frames += 1
                    frame_violence = True
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = detection.xyxy.cpu().numpy()[0]
                    # Draw bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    # Put label
                    label = f"Violence: {conf:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)

            # Write the annotated frame to the output video
            out.write(frame)
            frames_processed += 1

            # Calculate and send progress if websocket is provided
            if websocket:
                progress = int((frames_processed / total_frames) * 100)
                # Ensure progress does not exceed 100%
                progress = min(progress, 100)
                # Send progress update
                websocket.send_json({"progress": progress})

        cap.release()
        out.release()

        # Final progress update
        if websocket:
            websocket.send_json({"progress": 100})

        # Calculate violence percentage
        violence_percentage = (violence_detected_frames / frames_processed) * 100 if frames_processed > 0 else 0
        violence_detected = violence_percentage >= 40  # At least 40% frames detected violence

        return {
            'violenceDetected': violence_detected,
            'violencePercentage': round(violence_percentage, 2),
            'framesProcessed': frames_processed,
            'annotatedVideo': os.path.basename(output_path)  # Return the filename to serve via app
        }
