import cv2
import time
import threading
import config
from video_stream import VideoStream
from person_detection import PersonDetector
#from emergency_detection import EmergencyDetector
from video_storage import VideoStorage
from emergency_detection import EmergencyDetection
import os
import numpy as np
import send2trash
import tensorflow as tf

class SecuritySystem:
    def __init__(self):
        self.trash_temps()
        self.video_stream = VideoStream(config.DEBUG)
        
        self.person_detector = PersonDetector()
        #self.emergency_detector = EmergencyDetector()
        self.video_storage = VideoStorage()

        self.fgbg = cv2.createBackgroundSubtractorMOG2()

        self.segment_start_time = time.time()
        self.segment_count = 0
        self.video_storage.start_new_segment(self.segment_count)
        self.emergency_detector = EmergencyDetection()
        self.past = []

    def run(self):
        while True:
            frame, frame_display = self.video_stream.get_frame()
            if frame is None:
                break

            fgmask = self.fgbg.apply(frame)
            motion_detected = cv2.countNonZero(fgmask) > config.MOTION_THRESHOLD

            if motion_detected:
                print("Motion detected!")
                # Process frame for person detection
                processed_frame = self.person_detector.detect(frame)
                
                # Optional: Get current person count
                person_count = self.person_detector.get_person_count()
                print(f"Total unique persons tracked: {person_count}")
                
                # Update display with detections
                frame_display = processed_frame
                updated_frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_AREA)  # Correct size
                updated_frame = updated_frame / 255.0  # Normalize pixel values
                self.past.append(updated_frame)

                if len(self.past) == 16:
                    pred = self.emergency_detector.get_conf(self.past)
                    print(pred)
                    self.past = []

            
            self.video_storage.write_frame(frame)

            if time.time() - self.segment_start_time >= config.SEGMENT_DURATION:
                self.video_storage.close_segment()
                self.segment_count += 1
                self.segment_start_time = time.time()
                self.video_storage.start_new_segment(self.segment_count)

            cv2.imshow("Security Camera Feed", frame_display)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break            

        self.shutdown()

    def shutdown(self):
        self.video_stream.release()
        self.video_storage.close_segment()

        self.concat_videos()

        cv2.destroyAllWindows()

    def concat_videos(self):
        recordings_dir = config.VIDEO_SAVE_PATH
        final_dir = config.FINAL_VIDEO_SAVE_PATH
        
        os.makedirs(final_dir, exist_ok=True)
        
        segment_files = sorted(
            [f for f in os.listdir(recordings_dir) if f.endswith(".mp4")]
        )
        
        if not segment_files:
            print("No video segments found in the recordings directory.")
            return False

        final_output_path = os.path.join(final_dir, "final_video.mp4")

        try:
            first_video_path = os.path.join(recordings_dir, segment_files[0])
            cap = cv2.VideoCapture(first_video_path)

            if not cap.isOpened():
                print(f"Error: Unable to open first video file: {first_video_path}")
                return False

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = config.FRAME_RATE
            
            fourcc = cv2.VideoWriter_fourcc(*config.VIDEO_CODEC)
            out = cv2.VideoWriter(final_output_path, fourcc, fps, (frame_width, frame_height))

            cap.release() 

            for segment in segment_files:
                video_path = os.path.join(recordings_dir, segment)
                cap = cv2.VideoCapture(video_path)

                if not cap.isOpened():
                    print(f"Warning: Could not open segment {segment}. Skipping.")
                    continue

                current_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                current_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                if current_width != frame_width or current_height != frame_height:
                    print(f"Warning: Video {segment} has different dimensions. Skipping.")
                    cap.release()
                    continue

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)

                cap.release()

            out.release()
            print(f"Successfully created final video: {final_output_path}")
            return True

        except Exception as e:
            print(f"An error occurred during video concatenation: {e}")
            return False
        
    def trash_temps(self):
        folder_path = config.VIDEO_SAVE_PATH
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                send2trash.send2trash(file_path)


if __name__ == "__main__":
    system = SecuritySystem()
    system.run()