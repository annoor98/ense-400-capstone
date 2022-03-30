import numpy as np
import autopy


class tracker:

    def __init__(self, width, height):
        # Gets size of monitor
        self.monitorWidth = width
        self.monitorHeight = height

        # Creates a bounding box for mouse detection to work in
        self.boundx = 100
        self.boundy = 100
        self.mouseClicked = False

        # Mouse smoothing value
        self.smoothVal = 6
        self.prevX, self.prevY = 0, 0
        self.currX, self.currY = 0, 0

        self.camWidth, self.camHeight = 640, 480

    # Functions for hand gesture detection
    def isFist(self, landmarks):
        if landmarks[8][1] > (landmarks[6][1] + 10) and landmarks[12][1] > (landmarks[10][1] + 10) \
                and landmarks[16][1] > landmarks[14][1] and landmarks[20][1] > landmarks[18][1]:
            return True
        else:
            return False

    def isIndexUp(self, landmarks):
        if landmarks[8][1] < landmarks[6][1] - 20 and landmarks[12][1] < landmarks[9][1] - 20 \
                and landmarks[16][1] > landmarks[14][1] and landmarks[20][1] > landmarks[18][1]:
            return True
        else:
            return False

    def isOpenPalm(self, landmarks):
        if landmarks[8][1] < landmarks[6][1] and landmarks[12][1] < landmarks[9][1] \
                and landmarks[16][1] < landmarks[14][1] and landmarks[20][1] < landmarks[18][1] \
                and landmarks[16][1] < landmarks[6][1]:
            return True
        else:
            return False

    def isLeft(self, landmarks):
        if landmarks[8][0] > landmarks[6][0] and landmarks[12][0] > landmarks[9][0] \
                and landmarks[16][0] > landmarks[14][0] and landmarks[20][0] > landmarks[18][0] \
                and landmarks[16][1] > landmarks[6][1]:
            return True
        else:
            return False

    def isRight(self, landmarks):
        if landmarks[8][0] < landmarks[6][0] and landmarks[12][0] < landmarks[9][0] \
                and landmarks[16][0] < landmarks[14][0] and landmarks[20][0] < landmarks[18][0] \
                and landmarks[16][1] > landmarks[6][1]:
            return True
        else:
            return False

    def mouseDetect(self, landmarks):
        # Current location of the wrist
        palmX = landmarks[0][0]
        palmY = landmarks[0][1]

        # Prevents mouse from going out of bounds
        if palmX > self.monitorWidth - self.boundx:
            palmX = self.monitorWidth - self.boundx
        if palmX < self.boundx + 20:
            palmX = self.boundx + 20
        if palmY > self.monitorHeight - self.boundy:
            palmY = self.monitorHeight - self.boundy
        if palmY < self.boundy + 20:
            palmY = self.boundy + 20

        # Interpolates mouse position on screen relative to wrist position on camera feed
        x = np.interp(palmX, (self.boundx, self.camWidth - self.boundx), (0, self.monitorWidth))
        y = np.interp(palmY, (self.boundy, self.camHeight - self.boundy), (0, self.monitorHeight))


        # Smoothes out mouse movement
        self.currX = self.prevX + (x - self.prevX) / self.smoothVal
        self.currY = self.prevY + (y - self.prevY) / self.smoothVal

        # Updates mouse position
        autopy.mouse.move(self.monitorWidth - self.currX, self.currY)

        self.prevX, self.prevY = self.currX, self.currY

        # Another mouse click will not get triggered until an open palm is made again
        if self.isOpenPalm(landmarks):
            self.mouseClicked = False

    def mouseClick(self, landmarks):
        # Triggers a mouse click if a fist is made
        if self.isFist(landmarks) and self.mouseClicked is False:
            self.mouseClicked = True
            autopy.mouse.click()
