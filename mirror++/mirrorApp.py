import datetime
import time
import requests
import json
import speech_recognition as sr
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

from camera import camera
import calendarScreen as calendar

# Sets size of application screens
Window.size = (456, 810)
# Window.fullscreen = True

# Sets microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()
commandMode = False
gestures = True
voice = True
alarm = True

with open('devices.json', 'r') as file:
    devices = json.load(file)


# List of classes for every screen and widget component
class ClockLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.tState = 0

    def update(self, screen):
        pass


class TutorialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)


    def update(self, screen):
        pass


class TutorialScreen2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)


    def update(self, screen):
        pass


class CalendarScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.event1 = "No upcoming events"
        self.event2 = "No upcoming events"
        self.event3 = "No upcoming events"
        self.event4 = "No upcoming events"

        #self.event = calendar.getEvents()
        #if self.event:
         #   if self.event[0]:
          #      self.event1 = self.event[0]
           # if self.event[1]:
            #    self.event2 = self.event[1]
            #if self.event[2]:
             #   self.event3 = self.event[2]

    def update(self, screen):
        pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        #self.events = calendar.getEvents()
        self.firstEventText = "No Upcoming Event"

        #if self.events:
         #   self.firstEventText = self.events[0]
        #else:
         #   self.firstEventText = "No upcoming events"

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
        Clock.schedule_interval(self.update, 1)
        if calendar.getAlarmEvent():
            self.alarmTime = calendar.getAlarmEvent()[0]
        else:
            self.alarmTime = "No Alarms Present"

    def update(self, delta):
        self.alarmLight()

    def alarmLight(self):
        global alarm
        currentTime = datetime.datetime.now().strftime("%H:%M")
        if currentTime == self.alarmTime and alarm is True:
            requests.get(devices['lightsAlarm'])
            alarm = False


# ScreenManager class handles all other screens
class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.cam = mirrorApp.cam
        self.pollAudio()
        self.swiped = False

    def pollAudio(self):
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            print("Obtained audio...")

        stopListen = recognizer.listen_in_background(mic, self.audioCommand)


    def inputOption(self, i):
        global gestures, voice
        if i == 0:
            voice = False
            gestures = True
        elif i == 1:
            gestures = False
            voice = True
            Window.show_cursor = False
        else:
            voice = True
            gestures = True

        self.transition.direction = 'up'
        self.current = 'main'

    def audioCommand(self, rec, source):
        global commandMode, gestures
        if voice is False:
            return None
        try:
            word = rec.recognize_google(source)
            if commandMode is False:
                self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"

            if repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                if word == "voice only":
                    self.inputOption(1)
                elif word == "gestures only" or word == "gestures only":
                    self.inputOption(0)
                elif word == "both":
                    self.inputOption(2)

            if repr(self.current_screen) == "<Screen name='" + "tutorial" + "'>":
                if word == "next":
                    self.transition.direction = 'up'
                    self.current = 'tutorialVoice'
                    return None
            if repr(self.current_screen) == "<Screen name='" + "tutorialVoice" + "'>":
                if word == "next":
                    self.transition.direction = 'up'
                    self.current = 'settings'
                    return None


            if word == "mirror" and commandMode is False:
                commandMode = True
                self.get_screen('main').ids.command_label.text = "listening..."
            elif commandMode is True:
                if word == "alarm" or word == 'alarms':
                    self.transition.direction = 'up'
                    self.current = 'alarms'
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "guide":
                    self.transition.direction = 'up'
                    self.current = 'tutorial'
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "events":
                    self.transition.direction = 'up'
                    self.current = 'events'
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "settings":
                    self.transition.direction = 'up'
                    self.current = 'settings'
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "home":
                    self.transition.direction = 'up'
                    self.current = 'main'
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"
                    commandMode = False

                elif word == "toggle lights":
                    self.get_screen('main').ids.command_label.text = "Toggle Lights"
                    requests.get(devices['lights'])
                    commandMode = False
                elif word == "turn off gestures":
                    gestures = False
                    self.get_screen('main').ids.command_label.text = word
                    commandMode = False
                elif word == "turn on gestures":
                    gestures = True
                    self.get_screen('main').ids.command_label.text = word
                    commandMode = False
                else:
                    commandMode = False
                    self.get_screen('main').ids.command_label.text = "Say 'mirror' followed by a command!"

        except sr.UnknownValueError:
            print("Could not understand audio")
            commandMode = False
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    # Update function is called every 30sec
    def update(self, delta):
        # Updates camera tracking and logic
        global gestures
        if gestures is True:
            self.cam.run()
        if self.cam.gotoMain is True:
            if repr(self.current_screen) != "<Screen name='" + "main" + "'>":
                self.transition.direction = 'up'
                self.current = 'main'
        if self.cam.onScreen is True:
            self.gestureLogic()

    # Changes screen depending on direction and speed the hand swipes
    def gestureLogic(self):
        if self.cam.getGesture() == 5 and self.swiped is False:
            self.transition.direction = 'left'
            if repr(self.current_screen) == "<Screen name='" + "menu" + "'>":
                self.current = 'main'
            elif repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'settings'
            self.swiped = True
        elif self.cam.getGesture() == 4 and self.swiped is False:
            self.transition.direction = 'right'
            if repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'menu'
            elif repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                self.current = 'main'
            self.swiped = True
        elif self.cam.getGesture() != 4 and self.cam.getGesture() != 5:
            self.swiped = False


# Main application class
class mirrorApp(App):
    # Creates new camera object from camera class
    cam = camera(2)
    pass


mirrorApp().run()
