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

class Match_Form(forms.ModelForm):
    """Form for matching an unknown elephant
    The `Individual_Sighting` object associated with the unknown elephant is assigned to the `Individual` object associated with the match
    """
    class Meta:
        model = Individual_Sighting
        fields = ('individual',)
        # fields = '__all__'
    # indiv = None
    # indiv_sight = None

    def __init__(self, *args, **kwargs):
        self.indiv = kwargs.pop('indiv', None)
        self.indiv_sight = kwargs.pop('indiv_sight', None)
        super(Match_Form, self).__init__(*args, **kwargs)
        # if indiv:
        #     self.fields['indiv'].initial = indiv
        # if indiv_sight:
        #     self.fields['indiv_sight'].initial = indiv_sight

class Further_Review_Form(forms.ModelForm):
    class Meta:
        model = Individual_Sighting
        fields = ('completed',)
