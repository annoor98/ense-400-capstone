import numpy as np
import autopy

# Gets size of monitor
width, height = autopy.screen.size()

# Creates a bounding box for mouse detection to work in
boundx, boundy = 100, 100
mouseClicked = False

# Mouse smoothing value
smoothVal = 6
prevX, prevY = 0, 0
currX, currY = 0, 0

camWidth, camHeight = 640, 480


# Functions for hand gesture detection
def isFist(landmarks):
    if landmarks[8][1] > landmarks[6][1] and landmarks[12][1] > landmarks[10][1] \
            and landmarks[16][1] > landmarks[14][1] and landmarks[20][1] > landmarks[18][1]:
        return True
    else:
        return False


def isIndexUp(landmarks):
    if landmarks[8][1] < landmarks[6][1] and landmarks[12][1] > landmarks[9][1] \
            and landmarks[16][1] > landmarks[14][1] and landmarks[20][1] > landmarks[18][1]:
        return True
    else:
        return False


def isOpenPalm(landmarks):
    if landmarks[8][1] < landmarks[6][1] and landmarks[12][1] < landmarks[9][1] \
            and landmarks[16][1] < landmarks[14][1] and landmarks[20][1] < landmarks[18][1]:
        return True
    else:
        return False


def mouseDetect(landmarks):
    # Current location of the wrist
    palmX = landmarks[0][0]
    palmY = landmarks[0][1]

    # Prevents mouse from going out of bounds
    if palmX > 630 - boundx:
        palmX = 630 - boundx
    if palmX < boundx + 20:
        palmX = boundx + 20
    if palmY > 470 - boundy:
        palmY = 470 - boundy
    if palmY < boundy + 20:
        palmY = boundy + 20

    # Interpolates mouse position on screen relative to wrist position on camera feed
    x = np.interp(palmX, (boundx, camWidth - boundx), (0, width))
    y = np.interp(palmY, (boundy, camHeight - boundy), (0, height))

    global currX, currY, prevX, prevY
    global mouseClicked

    # Smoothes out mouse movement
    currX = prevX + (x - prevX) / smoothVal
    currY = prevY + (y - prevY) / smoothVal

    # Updates mouse position
    autopy.mouse.move(width - currX, currY)

    prevX, prevY = currX, currY

    # Triggers a mouse click if a fist is made
    if isFist(landmarks) and mouseClicked is False:
        mouseClicked = True
        autopy.mouse.click()

    # Another mouse click will not get triggered until an open palm is made again
    if isOpenPalm(landmarks):
        mouseClicked = False
