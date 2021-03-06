from django.urls import path, re_path, include
from app import views
from commons.integrations import gcalendar

urlpatterns = [
    # The home page
    path(
        '',
        views.index,
        name='home'
    ),
    path(
        'payment',
        views.payment,
        name='payment'
    ),
  
    path(
        'users',
        views.users,
        name='users'
    ),
    path(
        'appointments',
        views.appointments,
        name='appointments'
    ),
    path(
        'doctors',
        views.doctors,
        name='doctors'
    ),
    path(
        'doctors/<int:pk>/edit',
        views.doctors,
        name='doctors-edit'
    ),
    path(
        'prescriptions',
        views.prescriptions,
        name='prescriptions'
    ),
    path(
        'specialties',
        views.specialties,
        name='specialties'
    ),
    path(
        'specialties/add'
        , views.specialties,
        name='specialty_add'
    ),
    path(
        'integrations',
        views.integrations,
        name='integrations'
    ),

    # OAUTH2 GOOGLE CALENDAR
    path(
        "integrations/calendar/oauth2/google/redirect",
        gcalendar.AuthGoogle
    ),
    path(
        "integrations/mercado-pago/oauth2/redirect",
        views.mercado_pago
    ),
    path(
        "integrations/calendar/oauth2/google/callback",
        gcalendar.CallbackAuthGoogle
    ),
    path(
        "integrations/calendar/create",
        gcalendar.create_calendar
    ),
    path(
        "integrations/calendar/detail",
        gcalendar.get_calendar
    ),
    path(
        "integrations/calendar/freebuzy",
        gcalendar.get_freebusy
    ),
    path(
        "integrations/calendar/event/list",
        gcalendar.list_all_events
    ),
    path(
        "integrations/calendar/event/freetime",
        gcalendar.free_time
    ),

    # #
    # urls online reservation
    # #
    # path(
    #     "online/",
    #     views.list_online,
    #     name="online"
    # ),
    path(
        "online/upcoming_bookings",
        views.upcoming_bookings,
        name="upcoming_bookings"
    ),
    path(
        "online/upcoming/<int:booking_id>/attended", 
        views.atended_booking,
        name="attended"
    ),
    path(
        "online/<int:booking_id>/close/",
        views.close_booking,
        name="close_booking"
    ),
    #path(
    #    'profile',
    #    views.profile,
    #    name='profile'
    #),
   
    path(
        "profile",
        include(
            (
                [
                    path(
                        "",
                        views.profile,
                        name='profile'
                    ),
                    path(
                        "/edit",
                        views.update_profile,
                        name="edit"
                    )
                ],
                "profile",
            ), namespace="profile" 
        )

    ),
    
    path(
        "online",
        include(
            (
                [
                    path(
                        "",
                        views.list_online,
                        name="list"
                    ),
                    path(
                        "<int:booking_id>/detail",
                        views.detailOnline,
                        name="detail"
                    )
                ],
                "online"
            ), namespace="online"
        )
    ),
    path('pdf/<booking_pk>', views.generatePdf, name='pdf-receta')
]
