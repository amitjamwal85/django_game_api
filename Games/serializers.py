from rest_framework import serializers
from Games.models import Games, ContactUs


class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Games
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField( required=True )


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = '__all__'