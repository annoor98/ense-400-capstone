"""Main application file for Mirror++. Just run this python file to launch application."""
import datetime
import time
import json
import requests
import speech_recognition as sr
from kivy.app import App
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen

from camera import Camera
import events as events_screen
from weather import weather_result, temp_result, feel_result, forecast_result

# Sets size of application screen
WINDOWX = 456
WINDOWY = 810

Window.size = (WINDOWX, WINDOWY)
Window.fullscreen = True

# Sets microphone
recognizer = sr.Recognizer()
mic = sr.Microphone()
command_mode = False

gestures = True
voice = True
alarm = True
alarm_run = False
screen_off = False
command = "Say 'mirror' followed by a command!"

CAMERA_VAL = 1

with open('devices.json', 'r') as file:
    devices = json.load(file)


# ScreenManager class handles all other screens
class WindowManager(ScreenManager):
    """Kivy Window Manager that handles entire user interface"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.cam = mirrorApp.cam
        self.poll_audio()
        self.swiped = False

    def poll_audio(self):
        """function that polls audio in the background"""
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening...")
            print("Obtained audio...")

        # Listens for sound in the background in blocks of 2 second
        stopListen = recognizer.listen_in_background(mic, self.detect_voice_command, 2)

    def input_option(self, i):
        """Changes navigation type"""
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

    def toggle_iot_device(self, i):
        """Toggles IoT devices"""
        if i == 0:
            requests.get(devices['lights'])
        else:
            requests.get(devices['plugToggle'])

    def detect_voice_command(self, rec, source):
        """Function that detects commands in polled audio"""
        global command_mode, gestures, alarm_run, screen_off, command
        if voice is False:
            return None
        try:
            word = rec.recognize_google(source)
            if command_mode is False:
                command = "Say 'mirror' followed by a command!"

            if repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                if word == "voice only":
                    self.input_option(1)
                elif word == "gesture only" or word == "gestures only":
                    self.input_option(0)
                elif word == "both":
                    self.input_option(2)
                elif word == "screen off":
                    self.transition.direction = 'up'
                    self.current = 'blackscreen'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                    screen_off = True

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

            if word == "screen on" and screen_off is True:
                screen_off = False
                self.transition.direction = 'up'
                self.current = 'main'

            if word == "mirror" and command_mode is False and alarm_run is False:
                command_mode = True
                command = "listening..."

            elif command_mode is True and alarm_run is False:
                if word == "alarm" or word == 'alarms' and screen_off is False:
                    self.transition.direction = 'up'
                    self.current = 'alarms'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                elif word == "guide" and screen_off is False:
                    self.transition.direction = 'up'
                    self.current = 'tutorial'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                elif word == "screen off":
                    self.transition.direction = 'up'
                    self.current = 'blackscreen'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                    screen_off = True
                elif word == "events" and screen_off is False:
                    self.transition.direction = 'up'
                    self.current = 'events'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                elif word == "weather" and screen_off is False:
                    self.transition.direction = 'up'
                    self.current = 'weather'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                elif word == "settings" and screen_off is False:
                    self.transition.direction = 'up'
                    self.current = 'settings'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                elif word == "home":
                    self.transition.direction = 'up'
                    self.current = 'main'
                    command = "Say 'mirror' followed by a command!"
                    command_mode = False
                    screen_off = False

                elif word == "toggle light" and screen_off is False:
                    command = "Toggle Light"
                    self.toggle_iot_device(0)
                    command_mode = False
                elif word == "toggle switch" and screen_off is False:
                    command = "Toggle Switch"
                    self.toggle_iot_device(1)
                    command_mode = False
                elif word == "turn off gestures" and screen_off is False:
                    gestures = False
                    command = word
                    command_mode = False
                elif word == "turn on gestures" and screen_off is False:
                    gestures = True
                    command = word
                    command_mode = False
                else:
                    command_mode = False
                    command = "Say 'mirror' followed by a command!"
            elif word == "stop" and alarm_run is True:
                self.transition.direction = 'up'
                requests.get(devices['lightsAlarmOff'])
                self.current = 'main'
            print(word)
        except sr.UnknownValueError:
            print("Could not understand audio")
            command_mode = False
        except sr.RequestError as err:
            print("Sphinx error; {0}".format(err))

    # Update function is called every 30sec
    def update(self, delta):
        """Update function for Kivy classes. This one handles most logic"""
        # Updates camera tracking and logic
        global gestures, alarm_run
        if gestures is True:
            self.cam.run()
        if self.cam.go_to_main is True:
            if repr(self.current_screen) != "<Screen name='" + "main" + "'>":
                self.transition.direction = 'up'
                self.current = 'main'
        if self.cam.on_screen is True:
            self.detect_screen_change()

        if alarm_run:
            self.transition.direction = 'up'
            self.current = 'alarm'

        if mirrorApp.cam.get_hold_time() > 10:
            Window.set_system_cursor("crosshair")
        else:
            Window.set_system_cursor("hand")

    # Changes screen depending on hand gesture
    def detect_screen_change(self):
        """Function for changing screens depending on gesture"""
        global alarm_run
        if self.cam.get_gesture() == 5 and self.swiped is False and alarm_run is False:
            self.transition.direction = 'left'
            if repr(self.current_screen) == "<Screen name='" + "menu" + "'>":
                self.current = 'main'
            elif repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'settings'
            self.swiped = True
        elif self.cam.get_gesture() == 4 and self.swiped is False and alarm_run is False:
            self.transition.direction = 'right'
            if repr(self.current_screen) == "<Screen name='" + "main" + "'>":
                self.current = 'menu'
            elif repr(self.current_screen) == "<Screen name='" + "settings" + "'>":
                self.current = 'main'
            self.swiped = True
        elif self.cam.get_gesture() != 4 and self.cam.get_gesture() != 5 and alarm_run is False:
            self.swiped = False
        elif self.cam.get_gesture() == 3 and alarm_run is True:
            self.current = 'main'
            alarm_run = False
            requests.get(devices['lightsAlarmOff'])


class TutorialScreen(Screen):
    """First Tutorial Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, screen):
        """Update function for Kivy classes"""


class TutorialScreen2(Screen):
    """Second Tutorial Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, screen):
        """Update function for Kivy classes"""


class MainScreen(Screen):
    """Main Screen Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.events = events_screen.get_events()
        self.first_event_text = "No Upcoming Event"

        if self.events:
            self.first_event_text = self.events[0]
        else:
            self.first_event_text = "No upcoming events"

    def update(self, screen):
        """Update function for Kivy classes"""


class MenuScreen(Screen):
    """Menu Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        """Update function for Kivy classes"""


class IotScreen(Screen):
    """IoT Devices Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        """Update function for Kivy classes"""


class AlarmsScreen(Screen):
    """Alarms Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1)
        # if events_screen.get_alarm_event():
        #   self.alarm_time = events_screen.get_alarm_event()[0]
        # else:
        self.alarm_time = "No Alarms Present"

    def update(self, delta):
        """Update function for Kivy classes"""
        self.check_alarm()

    def check_alarm(self):
        """Function that checks if alarm should run"""
        global alarm, alarm_run
        currentTime = datetime.datetime.now().strftime("%H:%M")
        if currentTime == self.alarm_time and alarm is True:
            requests.get(devices['lightsAlarm'])
            alarm_run = True
            alarm = False
        if alarm_run is True:
            self.alarm_time = "ALARM RUNNING! SAY 'STOP' OR MAKE Home Gesture!"


class EventsScreen(Screen):
    """Events Widget Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)
        self.event1 = "No upcoming events"
        self.event2 = "No upcoming events"
        self.event3 = "No upcoming events"
        self.event4 = "No upcoming events"

        self.event = events_screen.get_events()
        if self.event:
            if self.event[0]:
                self.event1 = self.event[0]
            if self.event[1]:
                self.event2 = self.event[1]
            if self.event[2]:
                self.event3 = self.event[2]
            if self.event[3]:
                self.event4 = self.event[3]

    def update(self, screen):
        """Update function for Kivy classes"""


class WeatherScreen(Screen):
    """Weather Screen Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        """Update function for Kivy classes"""


class BlackScreen(Screen):
    """Black Screen Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, screen):
        """Update function for Kivy classes"""


class SettingsScreen(Screen):
    """Settings Screen Kivy Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, screen):
        """Update function for Kivy classes"""


class RoundedButton(Button):
    """Rounded Button Kivy Component"""

    def load_alarms(self):
        """Function to load alarm sound"""
        sound = SoundLoader.load('alarms/alarm_noise.wav')
        if ClockLabel.text == self.ids.test.text:
            sound.play()


class CommandLabel(Label):
    """Voice Command Kivy Label"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

    def update(self, delta):
        """Update function for Kivy classes. Updates text with voice commands"""
        global command, voice
        if voice is True:
            self.text = command
        else:
            self.text = ""


class ClockLabel(Label):
    """Clock Kivy Widget"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"
        Clock.schedule_interval(self.update, 1)

    def update(self, *args):
        """Update function for Kivy classes"""
        self.text = f"[u]{time.strftime('%I:%M:%S')}[/u]"


class WeatherIcon(Image):
    """Weather Icon Widget for Weather and main page"""

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
        """Update function for Kivy classes"""


class TempLabel(Label):
    """Temperature Kivy Label"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = temp_result + "°C"

    def update(self, delta):
        """Update function for Kivy classes"""


class WeatherLabel(Label):
    """Weather Kivy Label for Weather Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = weather_result

    def update(self, delta):
        """Update function for Kivy classes"""


class FeelsLabel(Label):
    """Feels Like Kivy Label for Weather Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = feel_result + "°C"

    def update(self, delta):
        """Update function for Kivy classes"""


class ForecastLabel(Label):
    """Forecast Label for Weather Page"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 30)

        self.text = forecast_result + "°C"

    def update(self, delta):
        """Update function for Kivy classes"""


# Main application class
class mirrorApp(App):
    # Creates new camera object from camera class
    cam = Camera(CAMERA_VAL)


mirrorApp().run()
