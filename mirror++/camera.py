"""Camera class runs the openCV module for gesture detection"""
import time
import cv2
import mediapipe as mp
from tracker import Tracker

CAMWIDTH = 640
CAMHEIGHT = 480
MONITORW = 2560
MONITORH = 1080


class Camera:
    """Camera class takes in id to determine which camera in system to use"""
    def __init__(self, cam_id):
        self.cam_width = CAMWIDTH
        self.cam_height = CAMHEIGHT

        self.capture = cv2.VideoCapture(cam_id, cv2.CAP_DSHOW)

        self.capture.set(3, self.cam_width)
        self.capture.set(4, self.cam_height)

        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(max_num_hands=1)

        self.is_palm = True
        self.on_screen = False

        # For fps tracking
        self.old_time = 0
        self.new_time = 0

        self.gesture_text = ""
        self.go_to_main = False
        self.gesture = 0
        self.hold_timer = 0
        self.hold_position = -1

        # 456,810
        self.tracker = Tracker(MONITORW, MONITORH, CAMWIDTH, CAMHEIGHT)

    def run(self):
        """Runs one frame of image processing"""
        success, img = self.capture.read()
        # convert image to rgb because hands only takes in rgb images
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        # If at least 1 hand is present in screen
        if results.multi_hand_landmarks:
            self.on_screen = True
            # Extract info of each hand (landmarks = location of hand) and draw points on screen
            for landmarks in results.multi_hand_landmarks:

                # Dictionary contains list of hand joints we'll be using for gesture calculation
                hand_landmarks = {
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
                for hid, land_m in enumerate(landmarks.landmark):
                    # Gets height, width and channel of our canvas
                    height, width, channel = img.shape
                    x_pos = int(land_m.x * width)
                    y_pos = int(land_m.y * height)

                    # Updates hand joints dictionary with each joints coordinates
                    if hid in hand_landmarks:
                        hand_landmarks[hid] = x_pos, y_pos

                self.tracker.update_landmark(hand_landmarks)

                # updates mouse position based on hand's joint positions
                self.tracker.mouse_detect()

                # Detects if hands are making any specific gestures
                self._gesture_detector()

                # Uncomment for dev testing
                self.mp_draw.draw_landmarks(img, landmarks, self.mp_hands.HAND_CONNECTIONS)
        else:
            self.gesture_text = "No Hands"
            self.on_screen = False

        # Gets framerate of camera
        self.new_time = time.time()
        fps = 1 / (self.new_time - self.old_time)
        self.old_time = self.new_time

        # Displays framerate on image feed (uncomment for dev testing)
        cv2.putText(img, self.gesture_text, (320, 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 3)
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

    def _gesture_detector(self):
        """Detects if hand is holding a gesture"""
        if self.tracker.is_fist():
            if self.hold_position == 2:
                self.hold_timer += 1
            else:
                self.hold_position = 2
                self.hold_timer = 0
            self.gesture_text = "FIST"
            if self.hold_timer > 25:
                self.gesture = 2
                self.hold_timer = 0
                self.tracker.mouse_click()
                self.is_palm = False
                self.go_to_main = False
        elif self.tracker.is_open_palm():
            self.gesture_text = "Open Palm"
            self.is_palm = True
            self.go_to_main = False
            self.gesture = 1
        elif self.tracker.is_peace_sign():
            if self.hold_position == 3:
                self.hold_timer += 1
            else:
                self.hold_position = 3
                self.hold_timer = 0
            self.gesture_text = "Peace Sign"
            if self.hold_timer > 25:
                self.gesture = 3
                self.hold_timer = 0
                self.go_to_main = True
        elif self.tracker.is_left():
            if self.hold_position == 4:
                self.hold_timer += 1
            else:
                self.hold_position = 4
                self.hold_timer = 0
            self.gesture_text = "LEFT"
            if self.hold_timer > 25:
                self.gesture = 4
                self.hold_timer = 0
        elif self.tracker.is_right():
            if self.hold_position == 5:
                self.hold_timer += 1
            else:
                self.hold_position = 5
                self.hold_timer = 0
            self.gesture_text = "RIGHT"
            if self.hold_timer > 25:
                self.gesture = 5
                self.hold_timer = 0
        else:
            self.hold_position = -1
            self.hold_timer = 0
            self.gesture_text = "NONE"
            self.go_to_main = False
            self.gesture = 0

    def get_gesture(self):
        """Returns which gesture is currently on camera feed"""
        return self.gesture
