from django.shortcuts import reverse
import django.contrib.auth.views as views
from django.contrib import messages


class SigninView(views.LoginView):
    template_name = "chat/sign-in.html"
    
    def get_success_url(self):
        return reverse("index")


class LogoutView(views.LogoutView):
    
    def get_success_url(self):
        return reverse("signin")