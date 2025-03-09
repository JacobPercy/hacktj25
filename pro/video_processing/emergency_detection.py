import os
import numpy as np
from tensorflow.keras.models import load_model
import config

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

import torch

if torch.cuda.is_available():
    print("CUDA is available.")

class EmergencyDetection:
    def __init__(self):
        try:
            self.model = load_model('model.keras')
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None
    
    def get_conf(self, frames):
        if self.model is None:
            print("Model is not loaded.")
            return None
        
        try:
            # Frames should already be a numpy array with shape (1, SEQUENCE_LENGTH, 64, 64, 3) from the SecuritySystem class
            pred = self.model.predict(frames)
            return pred
        except Exception as e:
            print(f"Error during prediction: {e}")
            print(f"Input shape: {frames.shape}")
            return None