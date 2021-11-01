

import requests

from django.conf import settings
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from payments.models import Payment
from .forms import StaffForm
from accounts.models import User, Profile
from commons.models import Specialty, IntegrationKey, Integration, Gender, Document_Type
from tenants.models import Booking, Staff, BookingDoctorDetailFile, BookingDoctorDetail
from .forms import  ProfileForm


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

# update user profile
@login_required(login_url="/login/")
def update_profile(request):
    profile = request.user.profile
    document = Document_Type.objects.all()
    gender = Gender.objects.all()
    form = ProfileForm(instance=profile)
	
    print(dir(form.fields["cell_phone"].widget))

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('/')

    print(document)
    context = {
        "form": form,
        # "profile": profile
        "document": document,
        "gender": gender
    }

    return render(request, 'profile/edit.html', context)


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
def mercado_pago(request):
    integration = Integration.objects.get(name="mercado pago")
    code = request.GET.get("code", None)
    data = {
        "client_secret": integration.key_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": integration.redirect,
    }
    resp = requests.post("https://api.mercadopago.com/oauth/token", data=data)
    if resp.status_code == 200:
        resp_json = resp.json()
        integration_key = IntegrationKey()
        integration_key.user = request.user
        integration_key.integration = integration
        integration_key.acceses_token = resp_json["access_token"]
        integration_key.token_refresh = resp_json["refresh_token"]
        integration_key.public_key = resp_json["public_key"]
        integration_key.last_token_update = timezone.now()
        integration_key.save()
    return HttpResponseRedirect('/integrations')


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
    staff = Staff.objects.all()
    context['staff'] = staff

    html_template = loader.get_template('doctors/index.html')
    return HttpResponse(html_template.render(context, request))


#     context = {}
#     context['segment'] = 'doctors'
# 
#     profile = Profile.objects.filter(is=True)
#     specialty = Specialty.objects.filter(is_active=True)
# 
#     context['profiles'] = profile
#     context['specialties'] = specialty
# 
#     html_template = loader.get_template('doctors/index.html')
#     return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def doctorUpdate(request):
    pass


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


@login_required(login_url="/login/")
def close_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking_detail = booking.booking_detail
        doctor_detail = getattr(booking_detail, "doctor_detail", None)
        description = request.POST.get("description")
        
        if doctor_detail is None:
            doctor_detail = BookingDoctorDetail.objects.create(booking_detail=booking_detail, description=description)
        else:
            doctor_detail.description=description
            doctor_detail.save()

        files = request.FILES.getlist("files", [])

        for file in files:
            BookingDoctorDetailFile.objects.create(booking_doctor_detail=doctor_detail, file=file)
            
        return redirect("online:list")
    
    context = {
        "booking": booking
    }

    return render(request, "online/close.html", context)

@login_required(login_url="/login/")
def upcoming_bookings(request):
    bookings = Booking.objects.all().order_by('-datetime')
    return render(request, "online/upcoming.html", {"bookings": bookings})
    # return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def list_online(request):
    patients = Booking.objects.all().order_by('-datetime')
    return render(request, "online/list.html", {"patients": patients})


@login_required(login_url="/login/")
def detailOnline(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 
        "online/detail.html", 
        {"booking": booking}
    )


@login_required(login_url="/login/")
def payment(request):
    context = {}
    context['segment'] = 'payment'

    payments = Payment.objects.all()
    print(payments)
    context['payments'] = payments

    # html_template = loader.get_template('payment/index.html')
    return render(request, "payment/index.html", {"payments": payments})
    # return HttpResponse(html_template.render(context, request))
