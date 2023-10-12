from flask import Flask, render_template
import cv2
import threading

app = Flask(__name__)

# Initialize the webcam capture
wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
frame = None
is_capturing = False

# Function to capture video from the webcam
def capture_video():
    global frame, is_capturing
    while is_capturing:
        success, img = cap.read()
        if success:
            frame = img

# Home route to display the webpage
@app.route('/')
def home():
    return render_template("index.html")

# Route to start capturing video
@app.route('/start_capture')
def start_capture():
    global is_capturing
    is_capturing = True
    capture_thread = threading.Thread(target=capture_video)
    capture_thread.start()
    return 'Capturing started'

# Route to stop capturing video
@app.route('/stop_capture')
def stop_capture():
    global is_capturing
    is_capturing = False
    return 'Capturing stopped'

# Route to display the captured video
@app.route('/video_feed')
def video_feed():
    return cv2.imencode('.jpg', frame)[1].tobytes()

if __name__ == '__main__':
    app.run(debug=True)
