import cv2
import os
import time
import config

class VideoStorage:
    def __init__(self):
        self.storage_path = config.VIDEO_SAVE_PATH
        os.makedirs(self.storage_path, exist_ok=True)  # Ensure directory exists
        self.video_writer = None
        self.current_filepath = None

    def start_new_segment(self, segment_count):
        """Starts a new video segment for continuous recording."""
        if self.video_writer:
            self.video_writer.release()  # Close the previous segment properly

        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"segment_{segment_count}_{timestamp}.mp4"
        self.current_filepath = os.path.join(self.storage_path, filename)

        fourcc = cv2.VideoWriter_fourcc(*config.VIDEO_CODEC)  # Ensure codec is set
        self.video_writer = cv2.VideoWriter(
            self.current_filepath,
            fourcc,
            config.FRAME_RATE,
            (config.FRAME_WIDTH, config.FRAME_HEIGHT)
        )

        if not self.video_writer.isOpened():
            print("Error: Failed to open VideoWriter!")
        else:
            print(f"Started new video segment: {self.current_filepath}")

    def write_frame(self, frame):
        """Writes a frame to the current video segment."""
        if self.video_writer is not None and frame is not None:
            self.video_writer.write(frame)

    def close_segment(self):
        """Releases the current video writer."""
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
            print(f"Closed segment: {self.current_filepath}")

    def save_event_clip(self, start_time, end_time, event_name):
        """Extracts and saves a short event clip using FFmpeg."""
        event_folder = os.path.join(self.storage_path, "events")
        os.makedirs(event_folder, exist_ok=True)

        event_filename = f"event_{event_name}_{start_time}.mp4"
        event_filepath = os.path.join(event_folder, event_filename)

        input_video = self.current_filepath  # Assuming event is from the latest segment

        # Run FFmpeg command to extract event clip (using system call)
        ffmpeg_command = f"ffmpeg -i {input_video} -ss {start_time} -to {end_time} -c copy {event_filepath}"
        os.system(ffmpeg_command)

        print(f"Saved event clip: {event_filepath} from {start_time} to {end_time}")
        return event_filepath