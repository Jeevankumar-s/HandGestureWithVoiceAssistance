from flask import Flask, render_template, Response
import cv2
import threading
import pygame
from fingerCountingProject import global_variable
import handTrackingModule as htm
import time

app = Flask(__name__)
pygame.init()
water_path = "water_audio.opus"
water_sound = pygame.mixer.Sound(water_path)

global_variable = None

# Initialize the webcam capture
wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
frame = None
is_capturing = False


def getNumber(ar):
    global global_variable
    s = ""
    for i in ar:
        s += str(ar[i]);

    if (s == "00000"):
        return (0)
    elif (s == "01000"):
        water_sound.play()
        pygame.time.delay(int(water_sound.get_length() * 1000))
        global_variable = water_sound
        return (1)
    elif (s == "01100"):
        food_sound.play()
        pygame.time.delay(int(food_sound.get_length() * 1000))
        global_variable = food_sound
        return (2)
    elif (s == "01110"):
        sleepy_sound.play()
        pygame.time.delay(int(sleepy_sound.get_length() * 1000))
        global_variable = sleepy_sound
        return (3)
    elif (s == "01111"):
        rest_sound.play()
        pygame.time.delay(int(rest_sound.get_length() * 1000))
        global_variable = rest_sound
        return (4)
    elif (s == "11111"):
        fruits_sound.play()
        pygame.time.delay(int(fruits_sound.get_length() * 1000))
        global_variable = fruits_sound
        return (5)
    elif (s == "01001"):
        return (6)
    elif (s == "01011"):
        return (7)


@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route to display the webpage
@app.route('/')
def home():
    return render_template("index.html")

def video_stream():
    global frame, is_capturing
    while is_capturing:
        success, img = cap.read()
        if success:
            frame = img
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


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
@app.route('/sound')
def sound_playing():
    global_variable.play()
    pygame.time.delay(int(global_variable.get_length() * 1000))
    return 'Sound Played'


# Route to display the captured video
@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


def capture_video():
    global frame
    pTime = 0
    detector = htm.handDetector(detectionCon=1)
    while is_capturing:
        success, img = cap.read()
        img = detector.findHands(img, draw=True)
        lmList = detector.findPosition(img, draw=False)

        fingers = []  # Placeholder for gesture recognition
        # Implement your gesture recognition logic here
        # For example, update the `fingers` list based on hand landmarks

        # Add code to play sounds or trigger actions based on recognized gestures
        if fingers == [1, 1, 0, 0, 0]:
            water_sound.play()
            pygame.time.delay(int(water_sound.get_length() * 1000))
            global_variable = water_sound

        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)
        cv2.imshow("image", img)
        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break


if __name__ == '__main__':
    app.run(debug=True)
