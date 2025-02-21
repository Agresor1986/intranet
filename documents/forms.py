from django import forms  # Importuje modul na vytváranie formulárov v Django
from .models import Document  # Importuje model Document
# Trieda formulára pre nahrávanie dokumentov
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document  # Určuje, že formulár bude založený na modeli Document
        fields = ('title', 'file',)  # Definuje polia, ktoré sa zobrazia vo formulári
    # Prispôsobenie formulára – pridanie popisov k poliam
    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)  # Zavolá pôvodnú inicializáciu formulára
        self.fields['title'].label = 'Názov'  # Nastaví popis pre pole "title"
        self.fields['file'].label = 'Súbor'  # Nastaví popis pre pole "file"


