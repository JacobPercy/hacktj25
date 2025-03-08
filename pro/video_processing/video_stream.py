import cv2
import config

class VideoStream:
    def __init__(self, debug_mode: bool):
        """
        Initialize the video stream. Will either open the webcam or a video file 
        based on the debug_mode setting.
        """
        self.debug_mode = debug_mode
        self.cap = None

        # If in debug mode, use the test video
        if self.debug_mode:
            self.cap = cv2.VideoCapture(config.VIDEO_SOURCE)
        else:
            # Open webcam (device 0, default)
            self.cap = cv2.VideoCapture(1)
        
        # Check if the video capture is opened correctly
        if not self.cap.isOpened():
            print("Error: Unable to access the video stream")
            exit()

        # Set capture resolution (for processing)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    def get_frame(self):
        """
        Retrieve the next frame from the video stream.
        Returns None if the video has ended.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None  # End of video or error
        
        # Resize the frame for processing (if needed)
        frame_resized_for_processing = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        
        # Resize for display
        frame_resized_for_display = cv2.resize(frame, (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))

        return frame_resized_for_processing, frame_resized_for_display

    def release(self):
        """
        Release the video capture object.
        """
        if self.cap:
            self.cap.release()
