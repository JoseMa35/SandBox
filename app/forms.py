from django.forms import ModelForm
from tenants.models import Staff, Booking


class StaffForm(ModelForm):
    class  Meta:
        model = Staff
        fields = "__all__"

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


