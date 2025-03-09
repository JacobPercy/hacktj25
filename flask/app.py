import cv2
from flask import Flask, Response, request, jsonify
import time
import collections
import requests

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
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

FLUTTER_APP_URL = "http://10.180.8.139:5001/notify"  # Change this

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
