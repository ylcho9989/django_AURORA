from django import forms
from .models import WebLink

class WebLinkForm(forms.ModelForm):
    class Meta:
        model = WebLink
        fields = ['name', 'url', 'category']
