from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.forms import PasswordChangeForm
import json
from PIL import Image


@login_required
@api_view(['GET'])
def profile(request):
    data = json.dumps({
        'userid': request.user.id, 
        'username': request.user.username, 
        'image': request.user.profile.image.url
    })

    return Response(data, status.HTTP_200_OK)


@login_required
@require_POST
def update_profile(request):
    image = request.FILES.get('image')
    username = request.POST.get('username')
    email = request.POST.get('email')
    old_password = request.POST.get('old_password')
    new_password1 = request.POST.get('new_password1')
    new_password2 = request.POST.get('new_password2')


    if image:
        request.user.profile.update_image(image)

    if username:
        request.user.username = username
        request.user.save()

    if email:
        request.user.email = email
        request.user.save()

    if old_password and new_password1 and new_password2:
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

    return redirect('index')


@login_required
@require_POST
def delete_profile(request):
    request.user.delete()

    return redirect('signup')