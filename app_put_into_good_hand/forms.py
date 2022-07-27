from django import forms
from app_put_into_good_hand.models import User


class RegisterForm(forms.Form):
    mail = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)



