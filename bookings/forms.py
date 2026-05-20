from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'customer_name',
            'customer_email',
            'check_in',
            'check_out'
        ]