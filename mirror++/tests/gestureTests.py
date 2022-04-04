import unittest
from camera import camera

cam = camera(1)


# Tests all 6 Gestures in sequential orders
# The 150 range is the fps of your camera * 10
# In our case our camera is 15fps so this gives us 10 seconds
class Test(unittest.TestCase):

    def testNoHands(self):
        print("Show No Hands in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i/15))
            cam.run()
        self.assertEqual(cam.gestureText, "No Hands")

    def testPalm(self):
        print("Make Open Palm in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i / 15))
            cam.run()
        self.assertEqual(cam.gestureText, "Open Palm")

    def testLeft(self):
        print("Make Left Sign in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i / 15))
            cam.run()
        self.assertEqual(cam.gestureText, "LEFT")

    def testRight(self):
        print("Make Right Sign in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i / 15))
            cam.run()
        self.assertEqual(cam.gestureText, "RIGHT")

    def testFist(self):
        print("Make Fist in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i / 15))
            cam.run()
        self.assertEqual(cam.gestureText, "FIST")

    def testPeace(self):
        print("Make Peace Sign in...")
        for i in range(150):
            if i % 15 == 0:
                print(10 - (i / 15))
            cam.run()
        self.assertEqual(cam.gestureText, "Peace Sign")


unittest.main()
