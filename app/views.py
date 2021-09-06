# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from accounts.models import User, Profile
from commons.models import Specialty, IntegrationKey, Integration


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
    integrations = Integration.objects.filter(is_active=True)
    context['integrations'] = integrations
    print(integrations)
    try:
        key = IntegrationKey.objects.get(user=request.user)
    except:
        key = None
    context['key'] = key
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

