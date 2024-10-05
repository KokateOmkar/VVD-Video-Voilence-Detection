import torch

class FightDetectionModel:
    def __init__(self, model_path):
        # Load the YOLOv8 model from the specified path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

    def detect(self, video_path):
        # Run the model on the video
        results = self.model(video_path)

        # Extract relevant information from results
        detected_classes = results.pred[0][:, -1].tolist()  # Detected classes
        boxes = results.pred[0][:, :4].tolist()  # Bounding boxes
        confidences = results.pred[0][:, 4].tolist()  # Confidence scores

        return {
            'boxes': boxes,
            'classes': detected_classes,
            'confidences': confidences,
            'original_image': results.imgs[0]  # This may be used to return an annotated image
        }
