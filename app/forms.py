from django.forms import ModelForm
from tenants.models import Staff, Booking
from accounts.models import Profile


class StaffForm(ModelForm):
    class  Meta:
        model = Staff
        fields = "__all__"

class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        # fields = "__all__"
        fields = [
            "full_name",
            "gender",
            "document_type",
            "document",
            "date_of_birth",
            "cell_phone",
            "address",
            "website",
            "about",
            "avatar",
            "signature",
            "email",
        ]
        
        def __init__(self, gender=None, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if gender:
                self.fields['gender'].choices = gender















