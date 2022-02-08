import datetime
import time
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from camera import camera
import speech

# Sets size of application screens
Window.size = (456, 810)


# List of classes for every screen and widget component
class ClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, screen):
        pass


class LightsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        pass


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        pass


class RoundedButton(Button):
    back_color = ListProperty()

    def change_color(self):
        if self.back_color == [1, 1, 1, 1]:
            self.back_color = [0, 1, 0, 1]
        else:
            self.back_color = [1, 1, 1, 1]

    def load_alarms(self):
        sound = SoundLoader.load('alarms/alarm_noise.wav')
        if ClockLabel.text == self.ids.test.text:
            sound.play()


class AlarmsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        pass


# ScreenManager class handles all other screens
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.cam = mirrorApp.cam

    def pollAudio(self, delta):
        print("HERERE")
        command = speech.pollAudio()
        if command == "light":
            self.transition.direction = 'up'
            self.current = 'lights'
        elif command == "home":
            if repr(self.current_screen) != "<Screen name='" + "main" + "'>":
                self.transition.direction = 'up'
                self.current = 'main'

    # Update function is called every 30sec
    def update(self, delta):
        # Updates camera tracking and logic
        self.cam.run()
        if self.cam.gotoMain is True:
            if repr(self.current_screen) != "<Screen name='" + "main" + "'>":
                self.transition.direction = 'up'
                self.current = 'main'
        if self.cam.onScreen is True:
            self.swipeLogic()

    # Changes screen depending on direction and speed the hand swipes
    def swipeLogic(self):
        oldPos, newPos = self.cam.getPosition()
        if self.cam.isPalm:
            if newPos > oldPos + 75 and oldPos != 0:
                self.transition.direction = 'right'
                if repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                    self.current = 'menu'
            elif newPos < oldPos - 75:
                self.transition.direction = 'left'
                if repr(self.current_screen) == "<Screen name='" + "menu" + "'>":
                    self.current = 'main'

        self.cam.setPosition(newPos)


# Main application class
class mirrorApp(App):
    # Creates new camera object from camera class
    cam = camera()
    pass


mirrorApp().run()
