"""Test class for testing the gestures"""
import unittest
from camera import Camera

# CAMERAVAL is the camera index in openCV
CAMERAVAL = 1
cam = Camera(CAMERAVAL)

CAMFPS = 15
TIMER = 5


# Tests all 6 Gestures in sequential orders
# The 150 range is the fps of your camera * 10
# In our case our camera is 15fps so this gives us 10 seconds
class Test(unittest.TestCase):

    def test_no_hands(self):
        print("Show No Hands in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "No Hands")

    def test_palm(self):
        print("Make Open Palm in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "Open Palm")

    def test_left(self):
        print("Make Left Sign in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "LEFT")

    def test_right(self):
        print("Make Right Sign in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "RIGHT")

    def test_fist(self):
        print("Make Fist in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "FIST")

    def test_peace(self):
        print("Make Peace Sign in...")
        for i in range(CAMFPS*TIMER):
            if i % CAMFPS == 0:
                print(TIMER - (i / CAMFPS))
            cam.run()
        self.assertEqual(cam.gesture_text, "Peace Sign")


unittest.main()
