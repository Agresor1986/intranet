from django import forms
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('title', 'file',)

    def __init__(self, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)

        # Nastavenie popisov pre jednotlivé polia
        self.fields['title'].label = 'Názov'
        self.fields['file'].label = 'Súbor'
