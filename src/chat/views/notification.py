from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from chat.models import FriendRequest
from django.core.serializers import serialize


def get_friend_request_data(friend_request):
    data = {}
    data['friendrequestid'] = friend_request.id
    data['otherusername']   = friend_request.user.username
    data['createdat']       = str(friend_request.created_at.date())
    return data


@api_view(['GET'])
def notifications(request):
    filter = request.GET['filter']

    if filter == 'all':
        query = FriendRequest.objects.filter(other=request.user, accepted=False)
    if filter == 'latest':
        query = FriendRequest.objects.filter(other=request.user, accepted=False).order_by('-created_at')[:20]
    if filter == 'oldest':
        query = FriendRequest.objects.filter(other=request.user, accepted=False).order_by('created_at')[:20]

    data = [get_friend_request_data(q) for q in query]
    data = JSONRenderer().render(data)

    return Response(data, status=status.HTTP_200_OK)


@login_required
@api_view(['POST'])
def accept_friend_request(request, id):
    friend_request = get_object_or_404(FriendRequest, id=id)
    friend_request.accepted = True
    friend_request.save()

    return Response(data={}, status=status.HTTP_201_CREATED)


@login_required
@api_view(['POST'])
def reject_friend_request(request, id):
    friend_request = get_object_or_404(FriendRequest, id=id)
    friend_request.delete()

    return Response(data={}, status=status.HTTP_200_OK)
