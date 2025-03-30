from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        help_text=''
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        help_text=''  
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
