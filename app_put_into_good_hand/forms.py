from django import forms


class RegisterForm(forms.Form):
    name = forms.CharField(label="Imię")
    surname = forms.CharField(label="Nazwisko")
    mail = forms.CharField(label="E-mail", widget=forms.EmailField)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)


class LoginForm(forms.Form):
    mail = forms.CharField(label="E-mail", widget=forms.EmailField)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)
