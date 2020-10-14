from rest_framework.serializers import ModelSerializer
from chat import models


class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'