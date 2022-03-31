from django import forms
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Contraseña"
            }
        )
    )
    password_repeat = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Repetir Contraseña"
            }
        )
    )

    class Meta:
        """Meta definition for MODELNAMEform."""
        model = User
        fields = (
            "username",
            "email",
            "names",
            "last_names",
            "genere",
        )


    def clean_password_repeat(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("password_repeat"):
            self.add_error("password_repeat", "Las contraseñas no son las mismas")

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder":"Username"
            }
        )
    )
    password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Contraseña"
            }
        )
    )


    def clean(self):
        cleaned_data = super(LoginForm,self).clean() #Sobrescribir los datos de esta variable
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if not authenticate(username=username,password=password):
            raise forms.ValidationError("Los datos de usuario no son correctos")
        return cleaned_data