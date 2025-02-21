from django.forms import ModelForm
from .models import *  # Importovanie všetkých modelov z aktuálnej aplikácie
from django import forms
# Definícia formulára pre vytvorenie nového fóra
class CreateInForum(ModelForm):
    class Meta:
        model = Forum  # Určenie modelu, na ktorom bude formulár založený
        fields = ['topic', 'description', 'link', 'file']  # Polia, ktoré budú zahrnuté vo formulári
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),  # Vlastná úprava poľa description na textarea s 5 riadkami
        }
    def __init__(self, *args, **kwargs):
        super(CreateInForum, self).__init__(*args, **kwargs)  # Inicializácia formuláru
        self.fields['topic'].label = 'Názov'  # Nastavenie popisu pre pole topic
        self.fields['description'].label = 'Popis'  # Nastavenie popisu pre pole description
        self.fields['link'].label = 'Odkaz'  # Nastavenie popisu pre pole link
        self.fields['file'].label = 'Súbor'  # Nastavenie popisu pre pole file
# Definícia formulára pre pridanie novej diskusie
class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion  # Určenie modelu, na ktorom bude formulár založený
        fields = ['discuss', 'link', 'file']  # Polia, ktoré budú zahrnuté vo formulári
    def __init__(self, *args, **kwargs):
        super(CreateInDiscussion, self).__init__(*args, **kwargs)  # Inicializácia formuláru
        self.fields['discuss'].label = 'Komentár'  # Nastavenie popisu pre pole discuss
        self.fields['link'].label = 'Odkaz'  # Nastavenie popisu pre pole link
        self.fields['file'].label = 'Súbor'  # Nastavenie popisu pre pole file
    def clean(self):
        cleaned_data = super().clean()  # Vyčistenie dát formuláru
        discuss = cleaned_data.get('discuss')  # Získanie hodnoty z poľa discuss
        link = cleaned_data.get('link')  # Získanie hodnoty z poľa link
        file = cleaned_data.get('file')  # Získanie hodnoty z poľa file
        # Kontrola, či aspoň jedno pole (discuss, link alebo file) bolo vyplnené
        if not (discuss or link or file):
            raise forms.ValidationError("Musíte zadať text, odkaz alebo pridať súbor.")
        return cleaned_data

