from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, View
from django.views.generic.edit import FormView

from .forms import LoginForm, UserRegisterForm
from .models import User

# Create your views here.

class UserRegisterView(FormView):
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        User.objects.create_user(
            username = form.cleaned_data.get("username"),
            email = form.cleaned_data.get("email"),
            password = form.cleaned_data.get("password"),
            names = form.cleaned_data.get("names"),
            last_names = form.cleaned_data.get("last_names"),
            genere = form.cleaned_data.get("genere"),
        )
        return super(UserRegisterView, self).form_valid(form)

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
