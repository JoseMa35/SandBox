from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "placeholder" : "Username",
    #             "class": "form-control"
    #         }
    #     ))
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name",
                "class": "form-control"
            }
        ))
    father_lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Father lastname",
                "class": "form-control"
            }
        ))
    mother_lastname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Mother lastname",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('name', 'father_lastname', 'mother_lastname', 'email', 'password1', 'password2')
