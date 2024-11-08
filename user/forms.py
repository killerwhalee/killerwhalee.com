from django import forms
from django.contrib.auth.forms import UserCreationForm

from user.models import User, Profile


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("image", "name")
