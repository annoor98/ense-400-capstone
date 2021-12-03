import cv2
import mediapipe as mp
import time
import requests

capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()
lightsRequest = "https://maker.ifttt.com/trigger/test1/with/key/ZCAepxROsA58ayIddbVXw"
isPalm = True

# for fps tracking
oldTime = 0
newTime = 0

gestureText = ""

handjoint = {
    "wrist": 0,
    "thumb": 4,
    "index": 8,
    "middle": 12,
    "ring": 16,
    "pinky": 20
}

# Boilerplate code for getting camera running
while True:
    success, img = capture.read()

    # convert image to rgb because hands only takes in rgb images
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)

    # if at least 1 hand is present in screen
    if results.multi_hand_landmarks:
        # extract info of each hand (landmarks = location of hand) and draw points on screen
        for landmarks in results.multi_hand_landmarks:

            # Dictionary contains list of hand joints we'll be using for fist gesture calculation
            fistCalc = {
                8: 0,
                12: 0,
                16: 0,
                20: 0,
                6: 0,
                10: 0,
                14: 0,
                18: 0
            }

            # gets individual point values
            for id, lm in enumerate(landmarks.landmark):
                # gets height, width and channel of our canvas
                height, width, channel = img.shape
                xPos = int(lm.x * width)
                yPos = int(lm.y * height)

                if id in fistCalc:
                    fistCalc[id] = yPos

                if id == handjoint["wrist"]:
                    cv2.circle(img, (xPos, yPos), 20, (255, 0, 255), cv2.FILLED)

            if fistCalc[8] > fistCalc[6] and fistCalc[12] > fistCalc[10]\
                    and fistCalc[16] > fistCalc[14] and fistCalc[20] > fistCalc[18]:
                gestureText = "Toggle Lights"
                if isPalm:
                    r = requests.get(lightsRequest)
                    isPalm = False
            else:
                gestureText = "Open Palm"
                isPalm = True


            mpDraw.draw_landmarks(img, landmarks, mpHands.HAND_CONNECTIONS)
    else:
        gestureText = ""

    newTime = time.time()
    fps = 1 / (newTime - oldTime)
    oldTime = newTime

    cv2.putText(img, gestureText, (320, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 3)
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
