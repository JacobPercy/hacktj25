import torch
import math
from ultralytics import YOLO

class FireDetection:
    def __init__(self, model_path='fire.pt'):
        self.model = YOLO(model_path)
        self.class_names = ["fire", "smoke"]
    
    def predict(self, frame):
        results = self.model(frame)
        highest_conf = 0
        print(results)
        #if(results != None and len(results[2])>0):
            #print("Fire detected")

        """
        for _, row in results.pandas().xyxy[0].iterrows():
            confidence = row['confidence']
            if confidence > highest_conf:
                highest_conf = confidence"""

        return None #highest_conf
