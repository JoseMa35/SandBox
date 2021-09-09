# Setup Google Calendar
from django.http import HttpResponse
from commons.models import IntegrationKey, Integration

import os
from django.shortcuts import HttpResponseRedirect

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

    print(calendar)
    print(calendar['kind'])
    print(calendar['timeMin'])
    print(calendar['timeMax'])

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


def free_time(request, pk):
    key = IntegrationKey.objects.get(integration__key=KEY, user__email='yahyr@gmail.com')
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

    startDate = datetime.datetime(year, month, day, open_hour, open_mins, tzinfo=pytz.timezone(TIME_ZONE))
    start = datetime.datetime.strftime(startDate, "%Y-%m-%dT%H:%M:%SZ")
    endDate = datetime.datetime(year, month, day, close_hour, close_mins, tzinfo=pytz.timezone(TIME_ZONE))
    end = datetime.datetime.strftime(endDate, "%Y-%m-%dT%H:%M:%SZ")

    if key.calendar_id is None:
        calendar_name = 'primary'
    else:
        calendar_name = key.calendar_id

    events_result = service.events().list(
        timeMax=end, calendarId=calendar_name,
        timeMin=start, singleEvents=True).execute()

    events = events_result.get('items', [])

    schedule_busy = []
    for event in events:
        item = {
            'date': request_date,
            'start_time': datetime.datetime.fromisoformat(event['start']['dateTime']).replace(
                tzinfo=pytz.timezone(TIME_ZONE)),
            'end_time': datetime.datetime.fromisoformat(event['end']['dateTime']).replace(
                tzinfo=pytz.timezone(TIME_ZONE)),
            'status': 'buzy'
        }
        schedule_busy.append(item)

    schedule = []
    current = startDate
    while current < endDate:
        current_one_mins = current + datetime.timedelta(minutes=(WORK_TIME_SCHEDULE - 1))
        more_current = current + datetime.timedelta(minutes=WORK_TIME_SCHEDULE)

        if len(schedule_busy) > 0:
            for event in schedule_busy:
                if current <= event['start_time'] <= current_one_mins or \
                        current <= event['end_time'] <= current_one_mins:
                    item = {
                        'date': request_date,
                        'start_time': current.time().strftime('%H:%M:%S'),
                        'end_time': more_current.time().strftime('%H:%M:%S'),
                        'status': 'buzy'
                    }
                    schedule.append(item)
                else:
                    item = {
                        'date': request_date,
                        'start_time': current.time().strftime('%H:%M:%S'),
                        'end_time': more_current.time().strftime('%H:%M:%S'),
                        'status': 'free'
                    }
                    schedule.append(item)
        else:
            item = {
                'date': request_date,
                'start_time': current.time().strftime('%H:%M:%S'),
                'end_time': more_current.time().strftime('%H:%M:%S'),
                'status': 'free'
            }
            schedule.append(item)
        current = more_current

    return HttpResponse(json.dumps(schedule, sort_keys=True))


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
