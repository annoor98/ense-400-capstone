from datetime import datetime, timezone, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

scopes = ['https://www.googleapis.com/auth/calendar']


def createCredentials():
    flow = InstalledAppFlow.from_client_secrets_file("calendarSecret.json", scopes=scopes)
    credentials = flow.run_console()

    pickle.dump(credentials, open("token.pkl", "wb"))


def getCredentials():
    credentials = pickle.load(open("token.pkl", "rb"))
    service = build("calendar", "v3", credentials=credentials)
    return service


def getEvents():
    localtime = datetime.now(timezone.utc).astimezone()
    localend = localtime + timedelta(days=2)

    startTime = localtime.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    endTime = localend.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

    service = getCredentials()
    calList = service.calendarList().list().execute()
    result = service.events().list(calendarId=calList['items'][1]['id'],
                                   timeMin=startTime, timeMax=endTime).execute()

    events = []
    for i in result['items']:
        events.append("Event:" + i['summary'] + "\nStart: " + i["start"]["date"] + "\nEnd: " + i["end"]["date"])
    return events


def getAlarmEvent():
    localtime = datetime.now(timezone.utc).astimezone()
    localend = localtime + timedelta(days=1)

    startTime = localtime.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"
    endTime = localend.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

    service = getCredentials()
    calList = service.calendarList().list().execute()
    result = service.events().list(calendarId=calList['items'][0]['id'],
                                   timeMin=startTime, timeMax=endTime).execute()
    event = []
    for i in result["items"]:
        event.append(i["start"]["dateTime"][11:16])
    return event

