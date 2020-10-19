import json
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@login_required
@api_view(['GET', 'POST'])
def profile(request):
    data = json.dumps({'userid': request.user.id, 'image': request.user.profile.image.url})

    return Response(data, status.HTTP_200_OK)