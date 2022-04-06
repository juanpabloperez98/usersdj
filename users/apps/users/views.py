from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView

from .forms import (LoginForm, UpdatePasswordForm, UserRegisterForm,
                    VerificationForm)
from .functions import code_generator
from .models import User

# Create your views here.

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"
    # Generate code


    def form_valid(self, form):
        code = code_generator()
        user = User.objects.create_user(
            username = form.cleaned_data.get("username"),
            email = form.cleaned_data.get("email"),
            password = form.cleaned_data.get("password"),
            names = form.cleaned_data.get("names"),
            last_names = form.cleaned_data.get("last_names"),
            genere = form.cleaned_data.get("genere"),
            code_register = code
        )
        # Enviar_codigo
        asunto = "Confirmar email"
        mensaje = "Codigo de verificacion: " +  code
        email_remitente = "juanpablo.perez@utp.edu.co"
        
        send_mail(asunto,mensaje,email_remitente,[form.cleaned_data.get("email"),])
        # Redirigir pantalla validacion
        return HttpResponseRedirect(
            reverse(
                "users_app:user-verification",
                kwargs={
                    "pk": user.id
                }
            )
        )


class Login(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home_app:panel")

    def form_valid(self, form):
        # Verify
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password"),
        )
        # Login
        login(self.request, user)
        return super(Login, self).form_valid(form)

class LogoutView(View):


    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse(
                "users_app:login"
            )
        )

class UpdatePassword(LoginRequiredMixin,FormView):
    template_name = "users/update.html"
    form_class = UpdatePasswordForm
    success_url = reverse_lazy("users_app:login")
    login_url = reverse_lazy("users_app:login")

    def get_form_kwargs(self):
        kwargs = super(UpdatePassword, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


    def form_valid(self, form):
        usuario = self.request.user
        new_pass = form.cleaned_data.get("new_password")
        usuario.set_password(new_pass)
        usuario.save()
        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)

class CodeVerificationView(FormView):
    template_name = "users/verification.html"
    form_class = VerificationForm
    success_url = reverse_lazy("users_app:login")

    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView,self).get_form_kwargs()
        kwargs.update({
            "pk":self.kwargs.get("pk")
        })
        return kwargs

    def form_valid(self, form):
        User.objects.filter(
            id=self.kwargs.get("pk")
        ).update(
            is_active = True
        )
        return super(CodeVerificationView, self).form_valid(form)
