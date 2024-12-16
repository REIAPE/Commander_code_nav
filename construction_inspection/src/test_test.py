import cv2 
import numpy as np
from time import time
from ultralytics import YOLO

class ObjectDetection:
    def __init__(self, capture_index):
        
        self.capture_index = capture_index
        self.device = 'cpu'
        print('Using Device: ', self.device)

        self.model = self.load_model()

    def load_model(self):
        model = YOLO("yolov8s.pt")
        model.fuse()

        return model
    
    def predict(self, frame):
        return self.model(frame)
    
    def plot_bboxes(self, results, frame):

        xyxyz = []
        confidences = []
        class_ids = []

        for result in results:
            boxes = result.boxes.cpu().numpy()

            xyxy = boxes.xyxy
            cv2.rectangle(frame, (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3])), (0,255,0), 2)

        return frame
    
    def __call__(self.capture_index):
        pass