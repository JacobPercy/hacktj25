from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Route to trigger notifications
@app.route('/send_notification')
def send_notification():
    print("Sending notification...")
    socketio.emit('new_notification', {'title': 'Test Notification', 'body': 'This is a test notification.'})
    return "Notification Sent"

# WebSocket event to connect clients
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('new_notification', {'title': 'Welcome!', 'body': 'You are now connected to the Flask server.'})

# WebSocket event to handle disconnections
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
