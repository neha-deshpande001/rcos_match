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

class Unknown_Individual_Form(forms.ModelForm):
    class Meta:
        model = Individual_Sighting
        fields = ('individual',)

class Selected_Match_Individual_Form(forms.ModelForm):
    class Meta:
        model = Individual_Sighting
        fields = ('individual',)

class Further_Review_Form(forms.ModelForm):
    class Meta:
        model = Individual_Sighting
        fields = ('completed',)
