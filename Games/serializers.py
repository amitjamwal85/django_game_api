from rest_framework import serializers
from Games.models import Games, ContactUs, AddS3File


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


class AddS3FileSerializer(serializers.Serializer):
    file = serializers.FileField( required=True )

    class Meta:
        model = AddS3File
        fields = ["file"]

    def create(self, validated_data):
        return AddS3File.objects.create(**validated_data)

    def get_allfiles(self):
        allfiles = AddS3File.objects.all()
        lst = []
        for allfile in allfiles:
            lst.append(allfile.file.url)
        return lst