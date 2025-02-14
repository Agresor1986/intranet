from django.forms import ModelForm
from .models import *
from django import forms

class CreateInForum(ModelForm):
    class Meta:
        model = Forum
        fields = ['topic', 'description', 'link', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(CreateInForum, self).__init__(*args, **kwargs)
        self.fields['topic'].label = 'Názov'
        self.fields['description'].label = 'Popis'
        self.fields['link'].label = 'Odkaz'
        self.fields['file'].label = 'Súbor'


class CreateInDiscussion(ModelForm):
    class Meta:
        model = Discussion
        fields = ['discuss', 'link', 'file']

    def __init__(self, *args, **kwargs):
        super(CreateInDiscussion, self).__init__(*args, **kwargs)
        self.fields['discuss'].label = 'Komentár'
        self.fields['link'].label = 'Odkaz'
        self.fields['file'].label = 'Súbor'

    def clean(self):
        cleaned_data = super().clean()
        discuss = cleaned_data.get('discuss')
        link = cleaned_data.get('link')
        file = cleaned_data.get('file')

        if not (discuss or link or file):
            raise forms.ValidationError("Musíte zadať text, odkaz alebo pridať súbor.")

        return cleaned_data
