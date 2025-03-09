# config.py

# Debug mode flag
DEBUG = True
FIGHT = False

# Video settings
CAMERA_INDEX = 0  # 0 for default webcam

if(FIGHT):
    VIDEO_SOURCE = "fight.mp4"  # Used in debug mode
else:
    VIDEO_SOURCE = "nofight.mp4"

FRAME_WIDTH = 640  # Width for initial frame capture
FRAME_HEIGHT = 480  # Height for initial frame capture
DISPLAY_WIDTH = 640  # Width for display
DISPLAY_HEIGHT = 480  # Height for display

# Motion detection settings
MOTION_THRESHOLD = 5000  # Minimum pixel change to consider as motion

# Video storage settings
SEGMENT_DURATION = 120  # Length of each saved video segment in seconds

VIDEO_SAVE_PATH = "video/recordings"  # Path to store full video recordings
FINAL_VIDEO_SAVE_PATH = "video/final"  # Path to store final concatenated video

EVENT_CLIP_PATH = "video/events"  # Path to store detected event clips
EVENT_CLIP_DURATION = 10  # Clip length in seconds (5 seconds before + 5 after event)

# Video encoding settings
VIDEO_CODEC = "mp4v"  # Codec for saving videos
FRAME_RATE = 15  # Frames per second for saved videos
LSTM_FRAME_COUNT = 64
SEQUENCE_LENGTH = 16
EMERGENCY_THRESHOLD = 0.95