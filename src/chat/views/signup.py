from django.shortcuts import render
from django.contrib import messages
from chat.forms import RegisterForm


def signup(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("signin")
        else:
            for error in form.errors:
                messages.error(request, form.errors[error])

    return render(request, "chat/sign-up.html")