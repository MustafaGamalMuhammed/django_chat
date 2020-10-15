from rest_framework.serializers import ModelSerializer
from chat import models


class MessageSerializer(ModelSerializer):
    class Meta:
        model = models.Message
        fields = '__all__'


class ContactSerializer(ModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'