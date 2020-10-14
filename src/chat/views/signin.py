from django.shortcuts import render, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib import messages


class SigninView(LoginView):
    template_name = "chat/sign-in.html"
    
    def get_success_url(self):
        return reverse("index")