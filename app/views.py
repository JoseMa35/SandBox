# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from accounts.models import User, Profile
from commons.models import Specialty

@login_required(login_url="/login/")
def index(request):
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def profile(request):
    context = {}
    context['segment'] = 'profile'

    html_template = loader.get_template('profile/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def users(request):
    context = {}
    context['segment'] = 'users'
    context['users'] = User.objects.all()
    html_template = loader.get_template('users/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def appointments(request):
    context = {}
    context['segment'] = 'appointments'

    html_template = loader.get_template('appointments/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def prescriptions(request):
    context = {}
    context['segment'] = 'prescriptions'

    html_template = loader.get_template('prescriptions/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def integrations(request):
    context = {}
    context['segment'] = 'integrations'

    html_template = loader.get_template('integrations/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def doctors(request):
    context = {}
    context['segment'] = 'doctors'

    profile = Profile.objects.filter(is_doctor=True)
    specialty = Specialty.objects.filter(is_active=True)

    context['profiles'] = profile
    context['specialties'] = specialty

    html_template = loader.get_template('doctors/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def specialties(request):
    context = {}
    context['segment'] = 'specialties'

    specialties = Specialty.objects.filter()
    context['specialties'] = specialties

    html_template = loader.get_template('specialties/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def specialty_form(request):
    context = {}
    context['segment'] = 'specialties'

    specialties = Specialty.objects.filter()
    context['specialties'] = specialties

    html_template = loader.get_template('specialties/index.html')
    return HttpResponse(html_template.render(context, request))


# Setup Google Calendar
import os
from django.shortcuts import HttpResponseRedirect

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = 'https://app-citas-medicas.herokuapp.com/integrations/calendar/oauth2/google/callback'
# REDIRECT_URI = 'http://localhost:8000/integrations/calendar/oauth2/google/callback'
JSON_FILEPATH = os.path.join(os.getcwd(), 'client_secret_web.apps.googleusercontent.com.json')

import google_apis_oauth
from googleapiclient.discovery import build
import datetime
import json


def RedirectOauthView(request):
    oauth_url = google_apis_oauth.get_authorization_url(
        JSON_FILEPATH, SCOPES, REDIRECT_URI)
    return HttpResponseRedirect(oauth_url)


# {"token": "ya29.a0ARrdaM_yeT1JElVf8CK_Te1JPiFwkzZXJwWSktdWpEFY7gQPi_fyU1wc6HybKoBTwNbaAKvVMtdDecuSZnNAZcQ0Jdc9H8dgPt8Gzqh5FEoDO68dXNnRfEYoAykPNOTRfOgwika36kw9i-WmjbSUVqhW22iP", "refresh_token": "1//0hDMnOvdZkPK7CgYIARAAGBESNwF-L9IrakZstp5zkmIhwnHNahVZ4jTdcD-roFuYdUQlUb2j_qSO_6GKBi784WLjoypkXOeoucU", "id_token": null, "token_uri": "https://oauth2.googleapis.com/token", "client_id": "676526299765-be6rcvs458njtgvdeitu4easbm4fmvd1.apps.googleusercontent.com", "client_secret": "KJXrfwhY7cVAkSTadwqOziPN", "scopes": ["https://www.googleapis.com/auth/calendar"], "expiry": "2021-08-19 08:56:33"}

def CallbackView(request):
    try:
        credentials = google_apis_oauth.get_crendentials_from_callback(
            request,
            JSON_FILEPATH,
            SCOPES,
            REDIRECT_URI
        )

        stringified_token = google_apis_oauth.stringify_credentials(
            credentials)
        return HttpResponse(stringified_token)

    except Exception as e:
        print(e)
        return HttpResponse(e)


def list(request):
    stringified_token = {
        "token": "ya29.a0ARrdaM_yeT1JElVf8CK_Te1JPiFwkzZXJwWSktdWpEFY7gQPi_fyU1wc6HybKoBTwNbaAKvVMtdDecuSZnNAZcQ0Jdc9H8dgPt8Gzqh5FEoDO68dXNnRfEYoAykPNOTRfOgwika36kw9i-WmjbSUVqhW22iP",
        "refresh_token": "1//0hDMnOvdZkPK7CgYIARAAGBESNwF-L9IrakZstp5zkmIhwnHNahVZ4jTdcD-roFuYdUQlUb2j_qSO_6GKBi784WLjoypkXOeoucU",
        "id_token": 'null', "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": "676526299765-be6rcvs458njtgvdeitu4easbm4fmvd1.apps.googleusercontent.com",
        "client_secret": "KJXrfwhY7cVAkSTadwqOziPN",
        "scopes": ["https://www.googleapis.com/auth/calendar"],
        "expiry": "2021-08-19 08:56:33"
    }

    creds = google_apis_oauth.load_credentials(json.dumps(stringified_token))

    # Using credentials to access Upcoming Events
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    print('Getting the upcoming 10 events')
    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return HttpResponse('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        return HttpResponse({start, event['summary']})
