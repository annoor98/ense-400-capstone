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
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from camera import camera
import calendarScreen as calendar
from weather import weather_result, temp_result, feel_result, forecast_result

# Sets size of application screens
# 456 810
Window.size = (456, 810)
# Window.fullscreen = True

# Sets microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()
commandMode = False
gestures = True
voice = True
alarm = True
alarmRun = False
screenOff = False
command = "Say 'mirror' followed by a command!"

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


class BlackScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

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

        # self.event = calendar.getEvents()
        # if self.event:
        #   if self.event[0]:
        #      self.event1 = self.event[0]
        # if self.event[1]:
        #    self.event2 = self.event[1]
        # if self.event[2]:
        #   self.event3 = self.event[2]

    def update(self, screen):
        pass


class WeatherIcon(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        if weather_result == "Rain":
            self.source = 'images/rainy.PNG'
        elif weather_result == "Clouds":
            self.source = 'images/cloudy.png'
        elif weather_result == "Snow":
            self.source = 'images/snowy.PNG'
        elif weather_result == "Clear":
            self.source = 'images/clear.PNG'
        else:
            self.source = 'images/sunny.PNG'

    def update(self, delta):
        pass


class TempLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = temp_result + "°C"

    def update(self, delta):
        pass


class WeatherLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = weather_result

    def update(self, delta):
        pass


class FeelsLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = feel_result + "°C"

    def update(self, delta):
        pass


class ForecastLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = forecast_result + "°C"

    def update(self, delta):
        pass


class WeatherScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        pass


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        # self.events = calendar.getEvents()
        self.firstEventText = "No Upcoming Event"

        # if self.events:
        #   self.firstEventText = self.events[0]
        # else:
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

    def load_alarms(self):
        sound = SoundLoader.load('alarms/alarm_noise.wav')
        if ClockLabel.text == self.ids.test.text:
            sound.play()


class CommandLabel(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        global command, voice
        if voice is True:
            self.text = command
        else:
            self.text = ""


class AlarmsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        # if calendar.getAlarmEvent():
        #   self.alarmTime = calendar.getAlarmEvent()[0]
        # else:
        self.alarmTime = "No Alarms Present"

    def update(self, delta):
        self.alarmLight()

    def alarmLight(self):
        global alarm, alarmRun
        currentTime = datetime.datetime.now().strftime("%H:%M")
        if currentTime == self.alarmTime and alarm is True:
            requests.get(devices['lightsAlarm'])
            alarmRun = True
            alarm = False
        if alarmRun is True:
            self.alarmTime = "ALARM RUNNING! SAY 'STOP' OR MAKE Home Gesture!"


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

    def toggleIoT(self, i):
        if i == 0:
            requests.get(devices['lights'])
        else:
            requests.get(devices['plugToggle'])

    def audioCommand(self, rec, source):
        global commandMode, gestures, alarmRun, screenOff, command
        if voice is False:
            return None
        try:
            word = rec.recognize_google(source)
            if commandMode is False:
                command = "Say 'mirror' followed by a command!"

            if repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                if word == "voice only":
                    self.inputOption(1)
                elif word == "gestures only" or word == "gestures only":
                    self.inputOption(0)
                elif word == "both":
                    self.inputOption(2)
                elif word == "screen off":
                    self.transition.direction = 'up'
                    self.current = 'blackscreen'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                    screenOff = True

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

            if word == "screen on" and screenOff is True:
                screenOff = False
                self.transition.direction = 'up'
                self.current = 'main'

            if word == "mirror" and commandMode is False and alarmRun is False:
                commandMode = True
                command = "listening..."

            elif commandMode is True and alarmRun is False:
                if word == "alarm" or word == 'alarms' and screenOff is False:
                    self.transition.direction = 'up'
                    self.current = 'alarms'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "guide" and screenOff is False:
                    self.transition.direction = 'up'
                    self.current = 'tutorial'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "screen off":
                    self.transition.direction = 'up'
                    self.current = 'blackscreen'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                    screenOff = True
                elif word == "events" and screenOff is False:
                    self.transition.direction = 'up'
                    self.current = 'events'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "weather" and screenOff is False:
                    self.transition.direction = 'up'
                    self.current = 'weather'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "settings" and screenOff is False:
                    self.transition.direction = 'up'
                    self.current = 'settings'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                elif word == "home":
                    self.transition.direction = 'up'
                    self.current = 'main'
                    command = "Say 'mirror' followed by a command!"
                    commandMode = False
                    screenOff = False

                elif word == "toggle light" and screenOff is False:
                    command = "Toggle Light"
                    self.toggleIoT(0)
                    commandMode = False
                elif word == "toggle switch" and screenOff is False:
                    command = "Toggle Switch"
                    self.toggleIoT(1)
                    commandMode = False
                elif word == "turn off gestures" and screenOff is False:
                    gestures = False
                    command = word
                    commandMode = False
                elif word == "turn on gestures" and screenOff is False:
                    gestures = True
                    command = word
                    commandMode = False
                else:
                    commandMode = False
                    command = "Say 'mirror' followed by a command!"
            elif word == "stop" and alarmRun is True:
                self.transition.direction = 'up'
                requests.get(devices['lightsAlarmOff'])
                self.current = 'main'
            print(word)
        except sr.UnknownValueError:
            print("Could not understand audio")
            commandMode = False
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    # Update function is called every 30sec
    def update(self, delta):
        # Updates camera tracking and logic
        global gestures, alarmRun
        if gestures is True:
            self.cam.run()
        if self.cam.gotoMain is True:
            if repr(self.current_screen) != "<Screen name='" + "main" + "'>":
                self.transition.direction = 'up'
                self.current = 'main'
        if self.cam.onScreen is True:
            self.gestureLogic()

        if alarmRun:
            self.transition.direction = 'up'
            self.current = 'alarm'

    # Changes screen depending on direction and speed the hand swipes
    def gestureLogic(self):
        global alarmRun
        if self.cam.getGesture() == 5 and self.swiped is False and alarmRun is False:
            self.transition.direction = 'left'
            if repr(self.current_screen) == "<Screen name='" + "menu" + "'>":
                self.current = 'main'
            elif repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'settings'
            self.swiped = True
        elif self.cam.getGesture() == 4 and self.swiped is False and alarmRun is False:
            self.transition.direction = 'right'
            if repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'menu'
            elif repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                self.current = 'main'
            self.swiped = True
        elif self.cam.getGesture() != 4 and self.cam.getGesture() != 5 and alarmRun is False:
            self.swiped = False
        elif self.cam.getGesture() == 3 and alarmRun is True:
            self.current = 'main'
            alarmRun = False
            requests.get(devices['lightsAlarmOff'])


# Main application class
class mirrorApp(App):
    # Creates new camera object from camera class
    cam = camera(1)


mirrorApp().run()
