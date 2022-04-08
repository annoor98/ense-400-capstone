"""Event script used to obtain events and alarms.
   Uses Google Calendar API"""
import pickle
from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes = ['https://www.googleapis.com/auth/calendar']


def create_credentials():
    """Creates a secret credential file via google login"""
    flow = InstalledAppFlow.from_client_secrets_file("eventsSecret.json", scopes=scopes)
    credentials = flow.run_console()

    pickle.dump(credentials, open("token.pkl", "wb"))


def get_credentials():
    """Gets credentials saved in pickle token file"""
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    return service


def get_events():
    """Gets events within the last 2 days"""
    localtime = datetime.now(timezone.utc).astimezone()
    localend = localtime + timedelta(days=2)

    start_time = localtime.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    end_time = localend.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

    service = get_credentials()
    cal_list = service.calendarList().list().execute()
    result = service.events().list(calendarId=cal_list['items'][1]['id'],
                                   timeMin=start_time, timeMax=end_time).execute()

    events = []
    for i in result['items']:
        events.append("Event: " + i['summary'] + "\nStart: "
                      + i["start"]["dateTime"][0:10] + " " + i["start"]["dateTime"][11:19]
                      + "\nEnd: " + i["end"]["dateTime"][0:10] + " "
                      + i["end"]["dateTime"][11:19])
    return events


def get_alarm_event():
    """Gets alarm events within the day"""
    local_time = datetime.now(timezone.utc).astimezone()
    local_end = local_time + timedelta(days=3)

    start_time = local_time.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    end_time = local_end.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

    service = get_credentials()
    cal_list = service.calendarList().list().execute()
    result = service.events().list(calendarId=cal_list['items'][0]['id'],
                                   timeMin=start_time, timeMax=end_time).execute()
    event = []
    for i in result["items"]:
        event.append(i["start"]["dateTime"][11:16])
    return event
