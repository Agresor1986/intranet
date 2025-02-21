from django import forms  
from cal.models import Event  # Import Event modelu
# Definícia formulára pre model Event
class EventForm(forms.ModelForm):
    class Meta:
        model = Event  # Určuje, že tento formulár pracuje s modelom Event
        widgets = {
            # Nastavuje typ input poľa pre dátum a čas
            'start_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': forms.DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        # Určuje, ktoré polia sa budú zobraziť v tomto formulári
        fields = ['title', 'description', 'start_time', 'end_time', 'color']
    # Inicializácia formulára a nastavenie vlastností jednotlivých polí
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # Nastavenie popisov pre jednotlivé polia
        self.fields['title'].label = 'Názov'
        self.fields['description'].label = 'Popis'
        self.fields['start_time'].label = 'Začiatok'
        self.fields['end_time'].label = 'Koniec'
        self.fields['color'].label = 'Typ'
        # Priradenie vlastných možností pre pole 'color' z modelu
        self.fields['color'].choices = Event.COLOR_CHOICES
        # Nastavenie formátov pre dátumy a časy
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

