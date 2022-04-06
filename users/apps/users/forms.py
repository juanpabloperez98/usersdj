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
    

class UpdatePasswordForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')  # To get request.user. Do not use kwargs.pop('user', None) due to potential security hole
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)


    last_password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Contraseña"
            }
        )
    )
    new_password = forms.CharField(
        label="Contraseña",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"Contraseña nueva"
            }
        )
    )

    def clean(self):
        cleaned_data = super(UpdatePasswordForm,self).clean() #Sobrescribir los datos de esta variable
        user = self.user
        user = authenticate(
            username=user.username,
            password=self.cleaned_data.get("last_password"),
        )
        if not user:
            raise forms.ValidationError("La contraseña anterior no es valida")
        return cleaned_data


class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)

    def __init__(self,pk,*args,**kwargs):
        self.id_user = pk
        super(VerificationForm,self).__init__(*args,**kwargs)

    def clean_codregistro(self):
        code = self.cleaned_data.get("codregistro")

        if len(code) == 6:
            activo = User.objects.cod_validation(
                self.id_user,
                code,
            )
            if not activo:
                raise forms.ValidationError("Codigo incorrecto")
        else:
            raise forms.ValidationError("Codigo incorrecto")

