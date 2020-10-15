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
    
    return data


@api_view(['GET'])
def contacts(request):
    filter = request.GET.get('filter')
    
    if filter == 'all':
        contacts = request.user.contacts.all()
    if filter == 'online':
        contacts = []
        for contact in request.user.contacts.all():
            if contact.other.profile.online():
                contacts.append(contact)
    if filter == 'offline':
        contacts = []
        for contact in request.user.contacts.all():
            if not contact.other.profile.online():
                contacts.append(contact)

    data = []
    
    for contact in contacts:
        data.append(get_contact_data(contact))
    
    data = JSONRenderer().render(data)

    return Response(data=data, status=status.HTTP_200_OK)