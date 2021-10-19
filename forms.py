from django import forms
from django.conf import settings

from eb_core.models import Individual_Sighting, Seek_Identity

class Seek_Identity_Form(forms.ModelForm):
    class Meta:
        model = Seek_Identity
        exclude = ('individual_sighting',)

    def save(self, individual_sighting=None, commit=True):
        instance = super(Seek_Identity_Form, self).save(commit=False)
        instance.individual_sighting = individual_sighting
        if commit:
            instance.save()
        return instance

class Completed_Form(forms.Form):
    """Form for user to select if the match is completed"""
    completed = forms.BooleanField(required=False)
