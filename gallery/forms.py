from django import forms
from .models import Explore

class ExploreForm(forms.ModelForm):
    class Meta:
        model = Explore
        fields = ['explore_title', 'explore_description']