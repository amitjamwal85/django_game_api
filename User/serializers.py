from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type

from User.models import Server, UserProfile, Post, Comments


class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super(TokenObtainPairSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        data['user'] = {
            'username': self.user.username,
            'email': self.user.email,
        }
        return data


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        data = {
            'access': text_type(refresh.access_token),
            # 'user': {
            # 'username': self.user.username,
            # 'email': self.user.email
            # }
        }

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()

            data['refresh'] = text_type(refresh)

        return data


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    last_login = serializers.DateTimeField(required=False, read_only=True)
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    is_staff = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'last_login', 'username', 'first_name', 'last_name', 'email', 'is_staff']


def required_and_valid(value):
    if value is None:
        raise serializers.ValidationError('This field is required')
    # verify its a valid email address
    # briteverify_email_request(email=value)
    return True


def required_field():
    return serializers.CharField(required=True)


def password_field():
    return serializers.CharField(
        max_length=32,
        min_length=8,
        required=True
    )


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[required_and_valid, UniqueValidator(queryset=User.objects.all())])
    password = password_field()
    first_name = required_field()
    last_name = required_field()

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['city', 'country']

    def get_profile(self, user):
        print(f"user : {user}")
        up = UserProfile.objects.get(user=user)
        user_profile = UserProfileSerializer(up)
        d = user_profile.data
        return d


##########################################################################################################


class ServerSerializer(serializers.ModelSerializer):
    """
    we can make field validation here and also make required using null=False in Model
    """
    price = serializers.CharField(required=True)
    plan_id = serializers.CharField(validators=[UniqueValidator(queryset=Server.objects.all())])

    class Meta:
        model = Server
        fields = '__all__'

    """
    to_representation auto called in case of get and list
    """
    # def to_representation(self, data):
    #     print(f"data : {data}")
    #     print(f"user : {self.context['request'].user}")
    #     return {
    #         'id': data.pk,
    #     }


    def get_server_filter(self, data):
        user = self.context['request'].user
        print(f"user: {user}")
        data['user'] = user.username
        print(f"data: {data}")
        return data


##########################################################################################################


class EmailSerializer(serializers.Serializer):
    recipient_list = serializers.ListField(required=True)
    email_body = serializers.CharField( required=True )
    email_subject = serializers.CharField( required=True )



class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = password_field()

# class PasswordSerializer(serializers.ModelSerializer):
#     password = password_field()
#
#     class Meta:
#         model = User
#         fields = ['password']


##########################################################################################################


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['post_title', 'post_text']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['comment']







