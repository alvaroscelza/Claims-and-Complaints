from django import forms
from .models import suggestions


class suggestionsForm(forms.ModelForm):
    class Meta:
        model = suggestions
        fields = ['text']
