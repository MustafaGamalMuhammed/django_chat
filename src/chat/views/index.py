from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from chat.models import FriendRequest



@login_required
def index(request):
    return render(request, 'chat/index.html')


@login_required
@require_POST
def friend_request(request):
    other = get_object_or_404(User, username=request.POST['username'])
    user = User.objects.get(id=request.POST['user'])

    FriendRequest.objects.get_or_create(user=user, other=other)

    return redirect("index")