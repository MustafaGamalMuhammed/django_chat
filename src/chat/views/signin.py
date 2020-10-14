from django.shortcuts import reverse, redirect
import django.contrib.auth as auth
import django.contrib.auth.views as views
from django.contrib import messages


class SigninView(views.LoginView):
    template_name = "chat/sign-in.html"
    
    def get_success_url(self):
        return reverse("index")


def logout(request):
    auth.logout(request)
    return redirect("index")