from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Task

class RegisterUser(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
    
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

class LoginUser(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class AddTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']

class PositionForm(forms.Form):
    position = forms.CharField()
