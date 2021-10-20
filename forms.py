from django import forms
from django.conf import settings


class Completed_Form(forms.Form):
    """Form for user to select if the match is completed"""
    completed = forms.BooleanField(required=False)
