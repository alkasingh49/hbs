from django import forms
from django.core.exceptions import ValidationError

from .models import Booking


class BookingForm(forms.ModelForm):
    def __init__(self, *args, room=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        self.user = user

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['check_in'].widget.attrs.update({'data-booking-start': 'true'})
        self.fields['check_out'].widget.attrs.update({'data-booking-end': 'true'})

    class Meta:
        model = Booking
        fields = [
            'check_in',
            'check_out',
        ]
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        booking = Booking(
            room=self.room,
            user=self.user,
            check_in=cleaned_data.get('check_in'),
            check_out=cleaned_data.get('check_out'),
        )

        try:
            booking.clean()
        except ValidationError as error:
            if hasattr(error, 'error_dict'):
                for field, messages in error.message_dict.items():
                    self.add_error(field if field in self.fields else None, messages)
            else:
                self.add_error(None, error)

        return cleaned_data
