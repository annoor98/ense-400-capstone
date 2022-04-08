"""Tracker class keeps track of gestures and cursor controls based on camera feed"""
import numpy as np
import autopy

BOUND = 20


class Tracker:
    """Tracker class takes the monitor and camera dimensions"""

    def __init__(self, cam_w, cam_h):
        # Gets size of monitor
        self.monitor_width, self.monitor_height = autopy.screen.size()

        # Creates a bounding box for mouse detection to work in
        self.bound_x = BOUND
        self.bound_y = BOUND
        self.mouse_clicked = False

        # Mouse smoothing value
        self.smooth_val = 6
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0

        self.cam_width, self.cam_height = cam_w, cam_h
        self.landmarks = None

    def update_landmark(self, landmarks):
        """Updates Hand Landmarks from camera feed"""
        self.landmarks = landmarks

    def is_fist(self):
        """Uses hand landmarks to detect if its making a fist"""
        if self.landmarks[8][1] > (self.landmarks[6][1] + 10) and \
                self.landmarks[12][1] > (self.landmarks[10][1] + 10) and \
                self.landmarks[16][1] > self.landmarks[14][1] and \
                self.landmarks[20][1] > self.landmarks[18][1]:
            return True
        return False

    def is_peace_sign(self):
        """Uses hand landmarks to detect if its making a peace sign"""
        if self.landmarks[8][1] < self.landmarks[6][1] - 20 and \
                self.landmarks[12][1] < self.landmarks[9][1] - 20 and \
                self.landmarks[16][1] > self.landmarks[14][1] and \
                self.landmarks[20][1] > self.landmarks[18][1]:
            return True
        return False

    def is_open_palm(self):
        """Uses hand landmarks to detect if its making an open palm"""
        if self.landmarks[8][1] < self.landmarks[6][1] and \
                self.landmarks[12][1] < self.landmarks[9][1] and \
                self.landmarks[16][1] < self.landmarks[14][1] and \
                self.landmarks[20][1] < self.landmarks[18][1] and \
                self.landmarks[16][1] < self.landmarks[6][1]:
            return True
        return False

    def is_left(self):
        """Uses hand landmarks to detect if its making a left gesture"""
        if self.landmarks[8][0] > self.landmarks[6][0] and \
                self.landmarks[12][0] > self.landmarks[9][0] and \
                self.landmarks[16][0] > self.landmarks[14][0] and \
                self.landmarks[20][0] > self.landmarks[18][0] and \
                self.landmarks[16][1] > self.landmarks[6][1]:
            return True
        return False

    def is_right(self):
        """Uses hand landmarks to detect if its making a right gesture"""
        if self.landmarks[8][0] < self.landmarks[6][0] and \
                self.landmarks[12][0] < self.landmarks[9][0] and \
                self.landmarks[16][0] < self.landmarks[14][0] and \
                self.landmarks[20][0] < self.landmarks[18][0] and \
                self.landmarks[16][1] > self.landmarks[6][1]:
            return True
        return False

    def mouse_detect(self):
        """Calculates cursor position based on tracked hand position on camera feed"""
        # Current location of the wrist
        palm_x = self.landmarks[0][0]
        palm_y = self.landmarks[0][1]

        # Updates Screen Size in case the resolution changes due to fullscreen
        self.monitor_width, self.monitor_height = autopy.screen.size()

        # Prevents mouse from going out of bounds
        if palm_x > self.cam_width - self.bound_x:
            palm_x = self.cam_width - self.bound_x
        if palm_x < self.bound_x + self.bound_x:
            palm_x = self.bound_x + self.bound_x
        if palm_y > self.cam_height - self.bound_y:
            palm_y = self.cam_height - self.bound_y
        if palm_y < self.bound_y + self.bound_y:
            palm_y = self.bound_y

        # Interpolates mouse position on screen relative to wrist position on camera feed
        mouse_x = np.interp(palm_x, (self.bound_x, self.cam_width - self.bound_x),
                            (0, self.monitor_width))
        mouse_y = np.interp(palm_y, (self.bound_y, self.cam_height - self.bound_y),
                            (0, self.monitor_height))

        # Smoothes out mouse movement
        self.curr_x = self.prev_x + (mouse_x - self.prev_x) / self.smooth_val
        self.curr_y = self.prev_y + (mouse_y - self.prev_y) / self.smooth_val

        # Updates mouse position
        autopy.mouse.move(self.monitor_width - self.curr_x, self.curr_y)

        self.prev_x, self.prev_y = self.curr_x, self.curr_y

        # Another mouse click will not get triggered until an open palm is made again
        if self.is_open_palm():
            self.mouse_clicked = False

    def mouse_click(self):
        """Triggers mouse click if fist gesture is detected"""
        if self.is_fist() and self.mouse_clicked is False:
            self.mouse_clicked = True
            autopy.mouse.click()
