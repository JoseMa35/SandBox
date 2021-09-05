# Setup Google Calendar
from django.http import HttpResponse
from django.utils import timezone
from commons.models import IntegrationKey, Integration

import os
from django.shortcuts import HttpResponseRedirect

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = 'https://app-citas-medicas.herokuapp.com/integrations/calendar/oauth2/google/callback'
# REDIRECT_URI = 'https://localhost:8000/integrations/calendar/oauth2/google/callback'
JSON_FILEPATH = os.path.join(os.getcwd(), 'client_secret_web.apps.googleusercontent.com.json')
KEY = 'gcalendar'
TIME_ZONE = 'America/Lima'

import google_apis_oauth
from googleapiclient.discovery import build
import datetime
import json


# Sing In whit google
def AuthGoogle(request):
    code = request.GET.get('code', None)

    if not code:
        raise Exception

    if code == KEY:
        oauth_url = google_apis_oauth.get_authorization_url(
            JSON_FILEPATH, SCOPES, REDIRECT_URI)

        return HttpResponseRedirect(oauth_url)


# Callback
def CallbackAuthGoogle(request):
    try:
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request, JSON_FILEPATH, SCOPES, REDIRECT_URI)
        stringified_token = google_apis_oauth \
            .stringify_credentials(credentials)

        integration = Integration.objects.get(key=KEY)
        IntegrationKey.objects.create(
            user=request.user,
            integration=integration,
            token=stringified_token
        )
        return HttpResponseRedirect('/integrations')
    except Exception as e:
        return HttpResponse(e)


# Create a calendar
def create_calendar(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user=request.user)
    # print(key.token)

    body = {
        'summary': 'TranviaTech',
        'timeZone': TIME_ZONE
    }

    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)
    created_calendar = service.calendars().insert(body=body).execute()

    # calendar = []
    # calendar.kind = created_calendar['kind']
    # calendar.etag = created_calendar['etag']
    # calendar.id = created_calendar['id']
    # calendar.summary = created_calendar['summary']
    # calendar.timeZone = created_calendar['timeZone']
    # calendar.conferenceProperties = created_calendar['conferenceProperties']
    # print(calendar)

    key.calendar = created_calendar
    key.calendar_id = created_calendar['id']
    key.save()
    return HttpResponse(created_calendar)


def get_calendar(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user=request.user)
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)
    calendar = service.calendars().get(calendarId=key.calendar_id).execute()
    return HttpResponse(calendar['summary'])


def get_freebusy(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user=request.user)
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)

    # This event should be returned by freebusy
    start = datetime.datetime(2021, 8, 6, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(2021, 8, 6, 23).strftime("%Y-%m-%dT%H:%M:%SZ")

    body = {
        "timeMin": start,
        "timeMax": end,
        "timeZone": TIME_ZONE,
        "items": [
            {"id": key.calendar_id},
        ]  #
    }
    calendar = service.freebusy().query(body=body).execute()

    print(calendar)
    return HttpResponse(calendar)


def list_all_events(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user=request.user)
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)

    start = datetime.datetime(2021, 8, 1, 0).strftime("%Y-%m-%dT%H:%M:%SZ")

    events_result = service.events().list(
        calendarId=key.calendar_id, timeMin=start,
        maxResults=20, singleEvents=True,
        orderBy='startTime').execute()

    print(events_result)

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return HttpResponse('No upcoming events found.')

    # start = []
    # for event in events:
    #     start.append(event['start'].get('dateTime', event['start'].get('date')))

    print(events)

    return HttpResponse(events)


def load_calendar(created_calendar):
    calendar = []
    calendar.kind = created_calendar.get('kind')
    calendar.etag = created_calendar.get('etag')
    calendar.id = created_calendar.get('id')
    calendar.summary = created_calendar.get('summary')
    calendar.timeZone = created_calendar.get('timeZone')
    calendar.conferenceProperties = created_calendar.get('conferenceProperties')
    return calendar


def stringify_calendar(calendar):
    calendar_dict = {
        'kind': calendar.kind,
        'etag': calendar.etag,
        'id': calendar.id,
        'summary': calendar.summary,
        'timeZone': calendar.timeZone,
        'conferenceProperties': calendar.conferenceProperties,
    }
    print(calendar_dict)
    return json.dumps(calendar_dict)
