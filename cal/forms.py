from django import forms
from cal.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title', 'description', 'start_time', 'end_time', 'color']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)

        # Nastavenie popisov pre jednotlivé polia
        self.fields['title'].label = 'Názov'
        self.fields['description'].label = 'Popis'
        self.fields['start_time'].label = 'Začiatok'
        self.fields['end_time'].label = 'Koniec'
        self.fields['color'].label = 'Farba'

        # Priradenie vlastných možností pre pole 'color' z modelu
        self.fields['color'].choices = Event.COLOR_CHOICES

        # input_formats na správne spracovanie dátumového a časového formátu
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)
