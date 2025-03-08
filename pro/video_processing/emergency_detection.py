import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

from tensorflow.keras.models import load_model
import config

class EmergencyDetection:
    def __init__(self):
        self.model = load_model('model.keras')
    
    def get_conf(self, frames):
        if(not(len(frames)==config.LSTM_FRAME_COUNT)):
            return
        pred = self.model.predict(frames)
        print(type(pred))
        return pred