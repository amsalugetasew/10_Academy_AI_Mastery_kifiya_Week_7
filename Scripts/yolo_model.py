# yolo_model.py

import cv2
import tensorflow as tf
import numpy as np
import logging
import time
from pathlib import Path
from yolov5 import YOLOv5

class YOLOModel:
    def __init__(self, model_path='yolov5s.pt', conf_threshold=0.5):
        self.model_path = model_path
        self.conf_threshold = conf_threshold
        self.model = None
        self._load_model()

        # Set up logging
        logging.basicConfig(filename='yolo_detection.log', level=logging.INFO)

    def _load_model(self):
        """Load the YOLO model using the YOLOv5 TensorFlow implementation."""
        try:
            # Load the model
            self.model = YOLOv5(self.model_path, device='cpu')
            logging.info(f"Model loaded from {self.model_path}")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")

    def detect_objects(self, image_path):
        """Detect objects in an image and return results."""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                logging.error(f"Error reading image: {image_path}")
                return []

            # Perform detection
            results = self.model.predict(img)

            # Filter results based on confidence threshold
            detected_objects = []
            for i, (xyxy, conf, cls) in enumerate(zip(results.xyxy[0], results.conf[0], results.cls[0])):
                if conf >= self.conf_threshold:
                    detected_objects.append({
                        'bounding_box': xyxy.tolist(),
                        'confidence': conf.item(),
                        'class': int(cls.item())
                    })

            logging.info(f"Detection results for {image_path}: {len(detected_objects)} objects detected.")
            return detected_objects

        except Exception as e:
            logging.error(f"Error in detection: {str(e)}")
            return []

    def save_detection_results(self, image_path, detections, db_connection):
        """Save detection results to database."""
        try:
            cursor = db_connection.cursor()
            for detection in detections:
                cursor.execute('''
                    INSERT INTO detections (image_path, bounding_box, confidence, class_label)
                    VALUES (?, ?, ?, ?)
                ''', (image_path, str(detection['bounding_box']), detection['confidence'], detection['class']))

            db_connection.commit()
            logging.info(f"Detection results saved for {image_path}")
        except Exception as e:
            logging.error(f"Error saving results: {str(e)}")
    
    def process_images(self, images, db_connection):
        """Process all images and store detection results in DB."""
        for image_path in images:
            detections = self.detect_objects(image_path)
            if detections:
                self.save_detection_results(image_path, detections, db_connection)
            else:
                logging.info(f"No objects detected in {image_path}")
