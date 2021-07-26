# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template

from accounts.models import User, Profile
from specialties.models import Specialty_Doctor


@login_required(login_url="/login/")
def index(request):
    
    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def profile(request):
    context = {}
    context['segment'] = 'profile'

    html_template = loader.get_template( 'profile/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def users(request):
    context = {}
    context['segment'] = 'users'
    users = User.objects.all()
    context['users'] = users
    print(context)

    html_template = loader.get_template( 'users/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def appointments(request):
    context = {}
    context['segment'] = 'appointments'

    html_template = loader.get_template( 'appointments/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def prescriptions(request):
    context = {}
    context['segment'] = 'prescriptions'

    html_template = loader.get_template( 'prescriptions/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def integrations(request):
    context = {}
    context['segment'] = 'integrations'

    html_template = loader.get_template( 'integrations/index.html' )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def doctors(request):
    context = {}
    context['segment'] = 'doctors'

    html_template = loader.get_template( 'doctors/index.html' )
    return HttpResponse(html_template.render(context, request))
