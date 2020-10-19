from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


def get_contact_data(contact):
    data = {}
    data['contactid']     = contact.id
    data['userid']        = contact.user.id
    data['roomname']      = contact.room.name
    data['roomid']        = contact.room.id
    data['otherusername'] = contact.other.username
    data['otherid']       = contact.other.id
    data['otheronline']   = contact.other.profile.online()
    data['otherimage']    = contact.other.profile.image.url

    return data


@api_view(['GET'])
def contacts(request):
    filter = request.GET.get('filter')
    
    if filter == 'all':
        contacts = request.user.contacts.all()
    if filter == 'online':
        contacts = [c for c in request.user.contacts.all() if c.other.profile.online()]
    if filter == 'offline':
        contacts = [c for c in request.user.contacts.all() if not c.other.profile.online()]

    data = [get_contact_data(c) for c in contacts]
    data = JSONRenderer().render(data)

    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
def search(request, search_query):
    contacts = request.user.contacts.filter(other__username__icontains=search_query)
    data = [get_contact_data(c) for c in contacts]    
    data = JSONRenderer().render(data)

    return Response(data=data, status=status.HTTP_200_OK)

