from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Room
from chat.serializers import MessageSerializer


@api_view(['GET'])
def messages(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = room.messages.order_by('-id')[:200]
    messages = reversed(messages)
    data = MessageSerializer(messages, many=True).data

    return Response(data=data, status=status.HTTP_200_OK)