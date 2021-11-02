import requests

from django.utils import timezone
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404, redirect

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from django import template

from payments.models import Payment
from tenants import StatusQoutes
from accounts.models import User
from .forms import ProfileForm
from commons.models import Specialty, IntegrationKey, Integration, Gender, Document_Type
from tenants.models import Booking, Staff, BookingDoctorDetailFile, BookingDoctorDetail, Tenant, TenantSettings


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


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile:profile') 
    context = {
        "form": form,
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

    bookingdoctordetails = BookingDoctorDetail.objects.all()
    context["bookingdoctordetails"] = bookingdoctordetails

    b = bookingdoctordetails[0]

    print(b.booking_detail.booking_id.doctor_id.profile.full_name)

    html_template = loader.get_template('prescriptions/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def integrations(request):
    context = {}
    integrations = Integration.objects.filter(is_active=True)
    context['integrations'] = integrations
    print(integrations)
    try:
        key = ""  # IntegrationKey.objects.get(user=request.user)
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
            doctor_detail.description = description
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
    user = request.user
    today = datetime.now().date()

    if user.profile.is_admin:
        bookings = Booking.objects.filter(datetime__gte=today, status__in=[0, 1, 2]) \
            .filter(tenant__staff__doctors__exact=user).order_by('-datetime')
    elif user.profile.is_doctor:
        bookings = Booking.objects.filter(datetime__gte=today, status__in=[0, 1, 2]) \
            .filter(doctor_id=user).order_by('-datetime')
    else:
        bookings = Booking.objects.filter(datetime__gte=today, status__in=[0, 1, 2]).order_by('-datetime')

    return render(request, "online/upcoming.html", {"bookings": bookings})


@login_required(login_url="/login/")
def atended_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = StatusQoutes.ATTENDED
    booking.save()

    # booking_status = Booking.status.ATTENDED
    # My code******************************************************************
    # return render(request, "online/attended.html")
    return redirect("/online/upcoming_bookings")

    # return render(request, "online/attended.html", {"bookings": booking_status})


from datetime import datetime, timedelta
from itertools import chain


@login_required(login_url="/login/")
def list_online(request):
    user = request.user
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    tomorrow = today + timedelta(1)

    if user.profile.is_admin:
        patients = Booking.objects.filter(datetime__lte=yesterday).filter(tenant__staff__doctors__exact=user).order_by(
            '-datetime')
        patients_now = Booking.objects.filter(datetime__range=(yesterday, tomorrow)).filter(
            status__in=[3, 4, 5]).filter(tenant__staff__doctors__exact=user)

    elif user.profile.is_doctor:
        patients = Booking.objects.filter(datetime__lte=yesterday).filter(doctor_id=user).order_by('-datetime')
        patients_now = Booking.objects.filter(datetime__range=(yesterday, tomorrow)).filter(
            status__in=[3, 4, 5]).filter(doctor_id=user)
    else:
        patients = Booking.objects.filter(datetime__lte=yesterday).order_by('-datetime')
        patients_now = Booking.objects.filter(datetime__range=(yesterday, tomorrow)).filter(
            status__in=[3, 4, 5]).filter(doctor_id=user)

    patients_list = list(chain(patients, patients_now))
    return render(request, "online/list.html", {"patients": patients_list})


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


from .utils import render_to_pdf


def generatePdf(request, booking_pk, *args, **kwargs):
    booking = Booking.objects.filter(pk=booking_pk).first()
    tenant = TenantSettings.objects.filter(tenant=booking.tenant).first()
    prescription = BookingDoctorDetail.objects.filter(booking_detail=booking_pk).first()
    data = {
        'booking': booking,
        'tenant': tenant,
        'prescription': prescription,
    }

    print(data)
    pdf = render_to_pdf('prescriptions/pdf/index.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
