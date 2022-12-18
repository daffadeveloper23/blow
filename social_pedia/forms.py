from django.forms import ModelForm
from django import forms
from .models import *

class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title', 'text', 'author', 'video']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'video': forms.FileInput(attrs={'class': 'form-control-file'})
        }