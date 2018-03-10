from django import forms

from .models import Register

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Register
        fields = ['username', 'email', 'course','password']