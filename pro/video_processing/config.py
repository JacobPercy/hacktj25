# config.py

# Debug mode flag
DEBUG = False
FIGHT = False

FIRE_TEST = False

# Video settings
CAMERA_INDEX = 0  # 0 for default webcam

if(FIGHT):
    VIDEO_SOURCE = "fight.mp4"
else:
    VIDEO_SOURCE = "nofight.mp4"

if(FIRE_TEST):
    DEBUG = True
    VIDEO_SOURCE = "fire.mp4"

FRAME_WIDTH = 640  
FRAME_HEIGHT = 480 
DISPLAY_WIDTH = 640 
DISPLAY_HEIGHT = 480 

MOTION_THRESHOLD = 5000  # Minimum pixel change to consider as motion

SEGMENT_DURATION = 120  

VIDEO_SAVE_PATH = "video/recordings"  
FINAL_VIDEO_SAVE_PATH = "video/final" 

VIDEO_CODEC = "mp4v"
FRAME_RATE = 15 
LSTM_FRAME_COUNT = 64
SEQUENCE_LENGTH = 16
EMERGENCY_THRESHOLD = 0.95