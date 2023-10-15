from flask import Flask, render_template, Response
import cv2
import threading
import pygame
import handTrackingModule as htm
import time

app = Flask(__name__)

pygame.init()
water_path = "water_audio.opus"
water_sound = pygame.mixer.Sound(water_path)

food_path = "food_audio.opus"
food_sound = pygame.mixer.Sound(food_path)

sleepy_path = "sleepy_audio.opus"
sleepy_sound = pygame.mixer.Sound(sleepy_path)

rest_path = "rest_audio.opus"
rest_sound = pygame.mixer.Sound(rest_path)

fruits_path = "fruits_audio.opus"
fruits_sound = pygame.mixer.Sound(fruits_path)
global_variable=None

# Define other sounds similarly

# Initialize the webcam capture
wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
frame = None
is_capturing = False

@app.route('/video_feed')
def video_feed():
    return Response(video_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route to display the webpage
@app.route('/')
def home():
    return render_template("index.html")

def video_stream():
    global frame, is_capturing
    pTime = 0
    def getNumber(ar):
        global global_variable
        s = ""
        for i in ar:
            s += str(ar[i])

        if (s == "00000"):
            return (0)
        elif (s == "01000"):
            # water_sound.play()
            # print("water")
            global_variable=water_sound
            # pygame.time.delay(int(water_sound.get_length() * 1000))
            return (1)
        elif (s == "01100"):
            # food_sound.play()
            # print("food")
            global_variable = food_sound
            # pygame.time.delay(int(food_sound.get_length() * 1000))
            return (2)
        elif (s == "01110"):
            # sleepy_sound.play()
            # print("sleep")
            global_variable = sleepy_sound
            # pygame.time.delay(int(sleepy_sound.get_length() * 1000))
            return (3)
        elif (s == "01111"):
            # rest_sound.play()
            # print("rest")
            global_variable = rest_sound
            # pygame.time.delay(int(rest_sound.get_length() * 1000))
            return (4)
        elif (s == "11111"):
            # fruits_sound.play()
            # print("fruits")
            global_variable = fruits_sound
            # pygame.time.delay(int(fruits_sound.get_length() * 1000))
            return (5)
        elif (s == "01001"):
            return (6)
        elif (s == "01011"):
            return (7)

    while is_capturing:
        success, img = cap.read()
        if success:
            frame = img

            # Initialize hand detection module
            detector = htm.handDetector(detectionCon=1)

            # Detect hands in the current frame
            img = detector.findHands(img, draw=True)
            lmList = detector.findPosition(img, draw=False)
            tipId = [4, 8, 12, 16, 20]
            if (len(lmList) != 0):
                fingers = []
                # thumb
                if (lmList[tipId[0]][1] > lmList[tipId[0] - 1][1]):
                    fingers.append(1)
                else:
                    fingers.append(0)
                for id in range(1, len(tipId)):
                    if (lmList[tipId[id]][2] < lmList[tipId[id] - 2][2]):
                        fingers.append(1)
                    else:
                        fingers.append(0)
                cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, str(getNumber(fingers)), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                            10, (255, 0, 0), 20)

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 3)

                # Encode the frame and yield it
                ret, jpeg = cv2.imencode('.jpg', img)
                if ret:
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/start_capture')
def start_capture():
    global is_capturing

    wcam, hcam = 640, 480
    cap = cv2.VideoCapture(0)
    cap.set(3, wcam)
    cap.set(4, hcam)

    is_capturing = True

    return 'Capturing started'

@app.route('/stop_capture')
def stop_capture():
    global is_capturing
    is_capturing = False
    return 'Capturing stopped'

@app.route('/sound')
def sound_playing():
    global global_variable
    global_variable.play()
    pygame.time.delay(int(global_variable.get_length() * 1000))
    return 'Sound Played'

if __name__ == '__main__':
    app.run(debug=True)
