from django.shortcuts import render


def signin(request):
    return render(request, "chat/sign-in.html")