import cv2
from flask import Flask, Response
import time
import collections

app = Flask(__name__)

camera = cv2.VideoCapture(0)

frame_queue = collections.deque(maxlen=2)

def generate_frames():
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        
        frame_bytes = jpeg.tobytes()
        
        frame_queue.append(frame_bytes)
        
        if len(frame_queue) == 2:
            time.sleep(5)
        
        if frame_queue:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_queue.popleft() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
