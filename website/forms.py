from datetime import time
from django import forms
from .models import Appointment
from datetime import date

AVAILABLE_TIMES = [
    (time(10, 0), "10:00 - 12:00"),
    (time(12, 0), "12:00 - 14:00"),
    (time(14, 0), "14:00 - 16:00"),
    (time(16, 0), "16:00 - 18:00"),
    (time(18, 0), "18:00 - 20:00"),
    (time(20, 0), "20:00 - 22:00"),
]


class AppointmentForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=[(t, _) for t, _ in AVAILABLE_TIMES],
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2'
        }),
        label="Vreme"
    )

    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'date', 'time']
        labels = {
            'date': 'Izaberi datum',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'value': 'Banesi',
                'placeholder': 'Ime',
                'class': 'w-full border border-gray-300 rounded px-4 py-2'
            }),
            'email': forms.EmailInput(attrs={
                'value': 'bane@gmail.com',
                'placeholder': 'Email',
                'class': 'w-full border border-gray-300 rounded px-4 py-2'
            }),
            'phone': forms.TextInput(attrs={
                'value': '01161235432',
                'placeholder': 'Telefon',
                'class': 'w-full border border-gray-300 rounded px-4 py-2'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': date.today().isoformat(),
                'class': 'w-full border border-gray-300 rounded px-4 py-2'
            })
        }
