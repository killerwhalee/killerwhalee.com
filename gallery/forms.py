from django import forms
from .models import Explore

class ExploreForm(forms.ModelForm):
    explore_cover_image = forms.ImageField(label='explore_cover_image', required=False)

    class Meta:
        model = Explore
        fields = ['explore_title', 'explore_description', 'explore_cover_image']