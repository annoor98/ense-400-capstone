import cv2
import mediapipe as mp
import time
from tracker import tracker


class camera:

    def __init__(self, cam_id):
        self.camWidth = 640
        self.camHeight = 480

        self.capture = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)

        self.capture.set(3, self.camWidth)
        self.capture.set(4, self.camHeight)

        self.mpHands = mp.solutions.hands
        self.mpDraw = mp.solutions.drawing_utils
        self.hands = self.mpHands.Hands(max_num_hands=1)

        self.isPalm = True
        self.onScreen = False

        # For fps tracking
        self.oldTime = 0
        self.newTime = 0

        self.gestureText = ""
        self.gotoMain = False
        self.gesture = 0
        self.holdTimer = 0
        self.holdPos = -1

        # 456,810
        self.tracker = tracker(1920, 1080)

    def run(self):
        success, img = self.capture.read()
        # convert image to rgb because hands only takes in rgb images
        imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imageRGB)

        # If at least 1 hand is present in screen
        if results.multi_hand_landmarks:
            self.onScreen = True
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

                # updates mouse position based on hand's joint positions
                self.tracker.mouseDetect(landmarkCalc)

                # Detects if hands are making any specific gestures
                if self.tracker.isFist(landmarkCalc):
                    if self.holdPos == 2:
                        self.holdTimer += 1
                    else:
                        self.holdPos = 2
                        self.holdTimer = 0
                    self.gestureText = "FIST"
                    if self.holdTimer > 25:
                        self.gesture = 2
                        self.holdTimer = 0
                        self.tracker.mouseClick(landmarkCalc)
                        self.isPalm = False
                        self.gotoMain = False
                elif self.tracker.isOpenPalm(landmarkCalc):
                    self.gestureText = "Open Palm"
                    self.isPalm = True
                    self.gotoMain = False
                    self.gesture = 1
                elif self.tracker.isIndexUp(landmarkCalc):
                    if self.holdPos == 3:
                        self.holdTimer += 1
                    else:
                        self.holdPos = 3
                        self.holdTimer = 0
                    self.gestureText = "Peace Sign"
                    if self.holdTimer > 25:
                        self.gesture = 3
                        self.holdTimer = 0
                        self.gotoMain = True
                elif self.tracker.isLeft(landmarkCalc):
                    if self.holdPos == 4:
                        self.holdTimer += 1
                    else:
                        self.holdPos = 4
                        self.holdTimer = 0
                    self.gestureText = "LEFT"
                    if self.holdTimer > 25:
                        self.gesture = 4
                        self.holdTimer = 0
                elif self.tracker.isRight(landmarkCalc):
                    if self.holdPos == 5:
                        self.holdTimer += 1
                    else:
                        self.holdPos = 5
                        self.holdTimer = 0
                    self.gestureText = "RIGHT"
                    if self.holdTimer > 25:
                        self.gesture = 5
                        self.holdTimer = 0
                else:
                    self.holdPos = -1
                    self.holdTimer = 0
                    self.gestureText = "NONE"
                    self.gotoMain = False
                    self.gesture = 0

                self.mpDraw.draw_landmarks(img, landmarks, self.mpHands.HAND_CONNECTIONS)
        else:
            self.gestureText = "No Hands"
            self.onScreen = False

        # Gets framerate of camera
        self.newTime = time.time()
        fps = 1 / (self.newTime - self.oldTime)
        self.oldTime = self.newTime

        # Displays framerate on image feed
        cv2.putText(img, self.gestureText, (320, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 3)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


    def getGesture(self):
        return self.gesture
