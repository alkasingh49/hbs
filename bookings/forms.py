from django import forms
from django.utils import timezone

from .models import Booking, Coupon


class BookingForm(forms.ModelForm):
    coupon_code = forms.CharField(
        required=False,
        label='Coupon code',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'Try WELCOME10',
            'autocomplete': 'off',
            'data-coupon-code': 'true',
        }),
    )

    def __init__(self, *args, room=None, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.room = room
        self.user = user
        self.coupon = None
        self.fields['check_in'].error_messages.update({
            'required': 'Please select a check-in date.',
            'invalid': 'Enter a valid check-in date.',
        })
        self.fields['check_out'].error_messages.update({
            'required': 'Please select a check-out date.',
            'invalid': 'Enter a valid check-out date.',
        })

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
        labels = {
            'check_in': 'Check-in date',
            'check_out': 'Check-out date',
        }
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_coupon_code(self):
        code = self.cleaned_data.get('coupon_code', '').strip().upper()

        if not code:
            return code

        try:
            self.coupon = Coupon.objects.get(code=code, active=True)
        except Coupon.DoesNotExist:
            raise forms.ValidationError('Enter a valid active coupon code.')

        return code

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if not check_in or not check_out:
            return cleaned_data

        if check_in and check_in < timezone.localdate():
            self.add_error('check_in', 'Check-in date cannot be in the past.')

        if check_out <= check_in:
            self.add_error('check_out', 'Check-out date must be after check-in date.')

        return cleaned_data
