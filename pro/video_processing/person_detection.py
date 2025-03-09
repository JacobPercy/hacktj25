import cv2
import numpy as np
import torch
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import os

# Correct import for DeepSORT
from deep_sort_realtime.deepsort_tracker import DeepSort

# YOLO imports
from ultralytics import YOLO

# Database setup
Base = declarative_base()

class PersonModel(Base):
    """SQLAlchemy model for storing person tracking information"""
    __tablename__ = 'persons'
    
    id = sa.Column(sa.Integer, primary_key=True)
    unique_tracking_id = sa.Column(sa.String, unique=True)
    feature_embedding = sa.Column(sa.PickleType)  # Store numpy array
    first_appearance = sa.Column(sa.DateTime, default=datetime.utcnow)
    total_appearances = sa.Column(sa.Integer, default=1)
    appearance_timestamps = sa.Column(sa.PickleType)  # List of timestamps

class PersonDetector:
    def __init__(self, db_path='db/persons.db'):
        """
        Initialize PersonDetector with:
        - YOLO for person detection
        - DeepSORT for tracking
        - SQLAlchemy for database management
        """
        # Ensure db directory exists
        os.makedirs('db', exist_ok=True)
        
        # YOLO model (using v8 for person detection)
        self.yolo_model = YOLO('yolov8s.pt')  # Nano version for performance
        
        # DeepSORT tracker (with default settings)
        self.tracker = DeepSort(max_age=60)
        
        # Database setup
        self.engine = sa.create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
        # Tracking state
        self.current_frame_detections = {}

    def detect(self, frame):
        """
        Main detection method:
        1. Use YOLO to detect persons
        2. Use DeepSORT for tracking
        3. Manage database entries
        
        :param frame: Input video frame
        :return: Processed frame with detections
        """
        # YOLO detection for persons
        yolo_results = self.yolo_model(frame, classes=[0])  # class 0 is person
        
        # Prepare detections for DeepSORT
        detections = []
        for result in yolo_results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                conf = float(box.conf[0])
                
                if conf < 0.9:
                    continue
                
                detections.append(([x1, y1, x2-x1, y2-y1], conf, None))
        
        # Track with DeepSORT
        tracks = self.tracker.update_tracks(detections, frame=frame)
        
        # Process and update database
        self._process_tracks(tracks, frame)
        
        # Draw bounding boxes
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = track.track_id
            ltrb = track.to_ltrb()
            
            cv2.rectangle(frame, 
                          (int(ltrb[0]), int(ltrb[1])), 
                          (int(ltrb[2]), int(ltrb[3])), 
                          (0, 255, 0), 2)
            cv2.putText(frame, f'ID: {track_id}', 
                        (int(ltrb[0]), int(ltrb[1]-10)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, 
                        (0, 255, 0), 2)
        
        return frame

    def _process_tracks(self, tracks, frame):
        """
        Process tracking results and update database
        
        :param tracks: DeepSORT tracks
        :param frame: Current frame
        """
        session = self.Session()
        
        for track in tracks:
            if not track.is_confirmed():
                continue
            
            track_id = str(track.track_id)
            
            # Check if person exists in database
            existing_person = session.query(PersonModel).filter_by(
                unique_tracking_id=track_id
            ).first()
            
            if existing_person:
                # Update existing person record
                existing_person.total_appearances += 1
                timestamps = existing_person.appearance_timestamps
                timestamps.append(datetime.utcnow())
                existing_person.appearance_timestamps = timestamps
            else:
                # Create new person record
                new_person = PersonModel(
                    unique_tracking_id=track_id,
                    feature_embedding=None,  # Placeholder
                    total_appearances=1,
                    appearance_timestamps=[datetime.utcnow()]
                )
                session.add(new_person)
            
        session.commit()
        session.close()

    def get_person_count(self):
        """
        Get total number of unique persons tracked
        
        :return: Number of unique persons in database
        """
        session = self.Session()
        count = session.query(PersonModel).count()
        session.close()
        return count