# Setup Google Calendar
from django.http import HttpResponse

from commons.models import IntegrationKey, Integration

import os
from django.shortcuts import HttpResponseRedirect
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = 'https://app-citas-medicas.herokuapp.com/integrations/calendar/oauth2/google/callback'
# REDIRECT_URI = 'https://localhost:8000/integrations/calendar/oauth2/google/callback'
JSON_FILEPATH = os.path.join(os.getcwd(), 'client_secret_web.apps.googleusercontent.com.json')
KEY = 'gcalendar'
TIME_ZONE = 'America/Lima'

OPEN_WORK_TIME = '08:00' or '08:00'
CLOSE_WORK_TIME = '18:00' or '18:00'

WORK_TIME_SCHEDULE = 30  # use mins

import google_apis_oauth
from googleapiclient.discovery import build
import datetime
import json
import pytz


def AuthGoogle(request):

    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI, consent_prompt=True)

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


def create_calendar(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user__pk=5)
    body = {
        'summary': 'TranviaTech',
        'timeZone': TIME_ZONE
    }

    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)
    created_calendar = service.calendars().insert(body=body).execute()

    key.calendar = created_calendar
    key.calendar_id = created_calendar['id']
    key.save()
    return HttpResponse(created_calendar)


def get_calendar(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user__pk=5)
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)
    calendar = service.calendars().get(calendarId='primary').execute()
    return HttpResponse(calendar['summary'])


def get_freebusy(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user__email='yahyr@gmail.com')
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)

    # This event should be returned by freebusy
    start = datetime.datetime(2021, 8, 6, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(2021, 8, 6, 23).strftime("%Y-%m-%dT%H:%M:%SZ")

    if key.calendar_id is None:
        calendar_name = 'primary'
    else:
        calendar_name = key.calendar_id

    body = {
        "timeMin": start,
        "timeMax": end,
        "timeZone": TIME_ZONE,
        "items": [
            {"id": calendar_name, "busy": 'Active'},
        ]  #
    }
    calendar = service.freebusy().query(body=body).execute()

    # print(calendar)
    # print(calendar['kind'])
    # print(calendar['timeMin'])
    # print(calendar['timeMax'])

    return HttpResponse(calendar)


def list_all_events(request):
    key = IntegrationKey.objects.get(integration__key=KEY, user__email='yahyr@gmail.com')
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)

    start = datetime.datetime(2021, 8, 6, 0).strftime("%Y-%m-%dT%H:%M:%SZ")
    end = datetime.datetime(2021, 8, 6, 23).strftime("%Y-%m-%dT%H:%M:%SZ")

    if key.calendar_id is None:
        calendar_name = 'primary'
    else:
        calendar_name = key.calendar_id

    events_result = service.events().list(
        calendarId=calendar_name, timeMin=start, timeMax=end,
        maxResults=20, singleEvents=True,
        orderBy='startTime').execute()

    # print(events_result)

    events = events_result.get('items', [])

    if not events:
        # print('No upcoming events found.')
        return HttpResponse('No upcoming events found.')

    return HttpResponse(events)


def free_time(request, pk):
    tz = pytz.timezone(TIME_ZONE)
    key = IntegrationKey.objects.get(integration__key=KEY, user__pk=pk)
    creds = google_apis_oauth.load_credentials(key.token)
    service = build('calendar', 'v3', credentials=creds)

    if 'date' in request.GET != None:
        request_date = request.GET['date']
        year = int(request_date.split('-')[0])
        month = int(request_date.split('-')[1])
        day = int(request_date.split('-')[2])
    else:
        return HttpResponse({'date param is required'}, status=400, )

    open_hour = int(OPEN_WORK_TIME.split(':')[0])
    open_mins = int(OPEN_WORK_TIME.split(':')[1])

    close_hour = int(CLOSE_WORK_TIME.split(':')[0])
    close_mins = int(CLOSE_WORK_TIME.split(':')[1])

    start_tz_datetime = tz.localize(datetime.datetime(year, month, day, open_hour, open_mins))
    end_tz_datetime = tz.localize(datetime.datetime(year, month, day, close_hour, close_mins))
    start = datetime.datetime.strftime(start_tz_datetime, "%Y-%m-%dT%H:%M:%S%z")
    end = datetime.datetime.strftime(end_tz_datetime, "%Y-%m-%dT%H:%M:%S%z")

    # print(start_tz_datetime)
    # print(end_tz_datetime)

    # if key.calendar_id is None:
    calendar_name = 'primary'  # use for defaut
    # else:
    #     calendar_name = key.calendar_id

    events_result = service.events().list(
        timeMin=start, timeMax=end, calendarId=calendar_name,
        singleEvents=True, timeZone=TIME_ZONE).execute()

    events = events_result.get('items', [])
    schedule_busy = []
    for event in events:
        item = {
            'date': request_date,
            'start_time': datetime.datetime.fromisoformat(event['start']['dateTime']),
            'end_time': datetime.datetime.fromisoformat(event['end']['dateTime']),
            'status': 'buzy'
        }
        # print({'START': event['start']['dateTime'], 'END': event['end']['dateTime']})
        schedule_busy.append(item)

    date_range = pd.date_range(start=start_tz_datetime, end=end_tz_datetime, freq=(str(WORK_TIME_SCHEDULE) + 'min'),
                               closed=None)
    # print(date_range)
    df = pd.DataFrame({'A': [x for x in range(date_range.size)]}, index=date_range)

    busy_pd = []
    for x in range(len(schedule_busy)):
        colition = df.between_time(
            start_time=schedule_busy[x]['start_time'].time(),
            end_time=schedule_busy[x]['end_time'].time(),
            include_start=True, include_end=False)

        basic = colition.values[:]
        # print('basic', basic[:])
        # print('basic', basic.size)
        for xi in basic:
            busy_pd.append(xi[0])

    # Generate list schedule free
    schedule = []
    for x in range(date_range.size - 1):
        # print(date_range[x])
        item = {
            'index': x,
            'date': request_date,
            'start_time': date_range[x].time().strftime('%H:%M:%S'),
            'end_time': date_range[x + 1].time().strftime('%H:%M:%S'),
            'status': 'free'
        }
        # print('FREE', item)
        schedule.append(item)

    # Change or remove free for buzy
    for item in schedule:
        for busy in busy_pd:
            if item['index'] == busy:
                item['status'] = 'buzy'

    return HttpResponse(json.dumps(schedule, sort_keys=True))
