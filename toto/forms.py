from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Lindatoto, Business, Post
from pyuploadcare.dj.forms import ImageField


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'lindatoto')


class LindatotoForm(forms.ModelForm):
    class Meta:
        model = Lindatoto
        exclude = ('admin',)


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        exclude = ('user', 'lindatoto')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user', 'toto')
