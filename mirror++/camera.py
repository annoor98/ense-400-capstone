import cv2
import mediapipe as mp
import time
import requests
import tracker as tracker


class camera:
    # Width and height of the webcam we are using. Feel free to change it
    camWidth, camHeight = 640, 480

    # First parameter determines which camera to use (0 is default)
    capture = cv2.VideoCapture(2, cv2.CAP_DSHOW)

    # Set width and height of frame
    capture.set(3, camWidth)
    capture.set(4, camHeight)

    mpHands = mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    hands = mpHands.Hands()

    lightsRequest = ""
    isPalm = True
    onScreen = False

    # Old and new positions of hand
    prevPos = 0
    newPos = 0

    # For fps tracking
    oldTime = 0
    newTime = 0

    gestureText = ""
    swipedRight = False
    swipedLeft = False
    gotoMain = False

    # Landmark positions for joints in a hand
    handjoint = {
        "wrist": 0,
        "thumb": 4,
        "index": 8,
        "middle": 12,
        "ring": 16,
        "pinky": 20
    }

    def run(self):
        success, img = camera.capture.read()
        # convert image to rgb because hands only takes in rgb images
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = camera.hands.process(imageRGB)

        # If at least 1 hand is present in screen
        if results.multi_hand_landmarks:
            if camera.onScreen is False:
                camera.prevPos = camera.newPos
                camera.onScreen = True
            # Extract info of each hand (landmarks = location of hand) and draw points on screen
            for landmarks in results.multi_hand_landmarks:

                # Dictionary contains list of hand joints we'll be using for fist gesture calculation
                landmarkCalc = {
                    0: 0,
                    1: 0,
                    4: 0,
                    8: 0,
                    9: 0,
                    12: 0,
                    16: 0,
                    20: 0,
                    6: 0,
                    10: 0,
                    14: 0,
                    18: 0
                }

                # Gets individual point values
                for hid, lm in enumerate(landmarks.landmark):
                    # Gets height, width and channel of our canvas
                    height, width, channel = img.shape
                    xPos = int(lm.x * width)
                    yPos = int(lm.y * height)

                    # Updates hand joints dictionary with each joints coordinates
                    if hid in landmarkCalc:
                        landmarkCalc[hid] = xPos, yPos

                    # Draws circle on the location of the wrist
                    if hid == camera.handjoint["wrist"]:
                        cv2.circle(img, (xPos, yPos), 20, (255, 0, 255), cv2.FILLED)
                        camera.newPos = xPos

                # updates mouse position based on hand's joint positions
                tracker.mouseDetect(landmarkCalc)

                # Detects if hands are making any specific gestures
                if tracker.isFist(landmarkCalc):
                    camera.gestureText = "Fist"
                    camera.isPalm = False
                    camera.gotoMain = False
                elif tracker.isOpenPalm(landmarkCalc):
                    camera.gestureText = "Open Palm"
                    camera.isPalm = True
                    camera.gotoMain = False
                elif tracker.isIndexUp(landmarkCalc):
                    camera.gestureText = "Index Up"
                    camera.gotoMain = True
                else:
                    camera.gestureText = "NONE"
                    camera.gotoMain = False

                camera.mpDraw.draw_landmarks(img, landmarks, camera.mpHands.HAND_CONNECTIONS)
        else:
            camera.gestureText = "No Hands"
            camera.onScreen = False
            camera.prevPos = 0

        # Gets framerate of camera
        camera.newTime = time.time()
        fps = 1 / (camera.newTime - camera.oldTime)
        camera.oldTime = camera.newTime

        # Displays framerate on image feed
        cv2.putText(img, camera.gestureText, (320, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 3)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    # Returns position of wrist
    def getPosition(self):
        return camera.prevPos, camera.newPos

    # Updates position of wrist
    def setPosition(self, pos):
        camera.prevPos = pos
