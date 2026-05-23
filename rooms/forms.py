from django import forms

from .models import Room


class RoomSearchForm(forms.Form):
    room_type = forms.ChoiceField(required=False, label='Room type')
    min_price = forms.IntegerField(required=False, min_value=0, label='Min price')
    max_price = forms.IntegerField(required=False, min_value=0, label='Max price')
    check_in = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    check_out = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    available_only = forms.BooleanField(
        required=False,
        label='Search available rooms only',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        room_types = Room.objects.order_by('room_type').values_list(
            'room_type',
            flat=True,
        ).distinct()

        self.fields['room_type'].choices = [('', 'Any type')] + [
            (room_type, room_type)
            for room_type in room_types
        ]

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['room_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['min_price'].widget.attrs.update({'placeholder': '0'})
        self.fields['max_price'].widget.attrs.update({'placeholder': '10000'})
        self.fields['available_only'].widget.attrs.update({
            'class': 'form-check-input',
        })

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if min_price is not None and max_price is not None and min_price > max_price:
            self.add_error('max_price', 'Maximum price must be greater than minimum price.')

        if bool(check_in) != bool(check_out):
            self.add_error('check_in', 'Select both check-in and check-out dates.')
            self.add_error('check_out', 'Select both check-in and check-out dates.')

        if check_in and check_out and check_out <= check_in:
            self.add_error('check_out', 'Check-out date must be after check-in date.')

        return cleaned_data


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'price', 'available']
        labels = {
            'room_number': 'Room Number',
            'room_type': 'Room Type',
            'price': 'Nightly Price',
            'available': 'Available',
        }
        widgets = {
            'room_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Price must be 0 or greater.')
        return price
