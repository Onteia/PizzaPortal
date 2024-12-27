from django import forms
from .models import Employee
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = (
            "username",
            "account_type",
            "password1",
            "password2",
        )
