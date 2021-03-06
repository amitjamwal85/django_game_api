from django.contrib.auth.models import User
from rest_framework import status, generics, mixins
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.viewsets import GenericViewSet
# from rolepermissions.checkers import has_permission
from rest_framework.schemas import AutoSchema, ManualSchema
from rest_framework_social_oauth2.views import ConvertTokenView
from oauth2_provider.models import AccessToken
from rest_framework.views import APIView
from DjangoDRF import settings
import json
import coreapi
import coreschema
from DjangoDRF.exceptions import TokenError, InvalidToken
from DjangoDRF.utils.sendEmail import ClassSendEmail
from User.models import Server, Post, Comments
from User.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, UserSerializer, RegistrationSerializer, \
    ServerSerializer, PasswordSerializer, UserProfileSerializer, PostSerializer, CommentSerializer, EmailSerializer, \
    SocialConvertTokenSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from six import text_type
from rest_framework.decorators import action
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import login
from User.utils import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView
import pickle
import numpy as np
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# from rolepermissions.roles import assign_role


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


class CustomSetPagination(PageNumberPagination):
    page_size = 10


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        data = serializer.validated_data
        serializer = UserProfileSerializer()
        user = User.objects.get(username=data.get("user").get("username"))
        login(request, user)
        user_profile = serializer.get_profile(user)
        data["profile"] = user_profile
        print(f'data: {data}')
        return Response(data, status=status.HTTP_200_OK)


class TokenRefreshView(TokenViewBase):
    serializer_class = TokenRefreshSerializer


############################################################################################################



class SocialConvertTokenView(ConvertTokenView, APIView):
    permission_classes = (AllowAny,)
    serializer_class = SocialConvertTokenSerializer
    schema = ManualSchema(
        fields=[
            coreapi.Field(
                name="grant_type",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='convert_token'
            ),
            coreapi.Field(
                "client_id",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='OAuth Application Client ID'
            ),
            coreapi.Field(
                "client_secret",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='OAuth Application Client Secret',
            ),
            coreapi.Field(
                "backend",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='facebook',
            ),
            coreapi.Field(
                "token",
                required=True,
                location="form",
                schema=coreschema.String(),
                description='Facebook Auth Token',
            ),
        ],
        description='Create Account from Facebook Auth Token',
        encoding='application/json'
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status_code = self.create_token_response(request._request)

        if 'error' in body:
            return Response(json.loads(body), status=status.HTTP_400_BAD_REQUEST)

        try:
            oauth_token = AccessToken.objects.get(token=json.loads(body).get('access_token'))
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        print("OAuth token user : ", oauth_token.user)

        token = RefreshToken.for_user(oauth_token.user)
        data = {
            'access': text_type(token.access_token),
            'refresh': text_type(token),
            'expiry_time': settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        }
        return Response(data, status=status.HTTP_201_CREATED)


############################################################################################################


class UserAPIView(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = 'pk'

    @action(methods=['post'],
            detail=False,
            permission_classes=[AllowAny],
            url_path='register',
            url_name='register',
            serializer_class=RegistrationSerializer)
    def register(self, request):
        """
        To register a new user account
        """
        data = request.data
        print(f"data:{data}")
        serializer = RegistrationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(validated_data=serializer.validated_data)
            token = RefreshToken.for_user(user)

            # assign_role(user, data.get("role"))
            user = serializer.data
            user_id = User.objects.get(username=user['username'])
            user['user_id'] = user_id.id
            data = {
                'access': text_type(token.access_token),
                'refresh': text_type(token),
                'user': user,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @action( detail=False,
    #          methods=['POST'],
    #          permission_classes=[IsAuthenticated],
    #          serializer_class=PasswordSerializer,
    #          url_path='check-permission',
    #          url_name='check-permission',
    #          )
    # def check_permission(self, request):
    #     user = self.request.user
    #     l = user.groups.values_list( 'name', flat=True )
    #     l_as_list = list( l )
    #     print( f" group : {l_as_list}" )
    #     print( f"check permission {has_permission( user, 'view_posts' )}" )
    #     return Response(
    #         {"status": "success"}, status=status.HTTP_200_OK
    #     )

    @action(detail=False,
            methods=['POST'],
            serializer_class=PasswordSerializer
            )
    def update_password(self, request):
        user = self.request.user
        # print(f'user: {user}')
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # print(f'serializer : {serializer.data.get("new_password")}')
            if not user.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": "Wrong password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response(
                {"status": "success"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'],
            detail=False,
            permission_classes=[AllowAny],
            url_path='sendemail',
            url_name='sendemail',
            serializer_class=EmailSerializer)
    def sendemail(self, request):
        data = request.data
        serializer = EmailSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            sendEmail = ClassSendEmail(data)
            resp = sendEmail.SendEmail()
            if resp:
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################################################################################################


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


############################################################################################################

class PostView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "pk"
    pagination_class = CustomSetPagination

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        print(f"user : {user}")
        instance = self.get_object()
        print(f'instance = {instance.id}')
        serializer = self.get_serializer(instance)
        return_data = serializer.data
        comment_list = list()
        comments = Comments.objects.filter(post=instance)
        for comment in comments:
            data = dict()
            data['comment'] = comment.comment
            comment_list.append(data)
        return_data['comments'] = comment_list
        return Response(return_data)

    def create(self, request, *args, **kwargs):
        print(f"data: {request.data}")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["user"] = request.user
        serializer.create(validated_data=validated_data)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)

    @action(methods=['post'],
            detail=True,
            permission_classes=[IsAuthenticated],
            url_name="comment",
            url_path="comment",
            serializer_class=CommentSerializer
            )
    def add_comment(self, request, pk=None):
        post_obj = self.get_object()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data["post"] = post_obj
        serializer.create(validated_data=validated_data)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)


############################################################################################################


class ServerView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ServerSerializer
    queryset = Server.objects.all()
    lookup_field = 'pk'
    pagination_class = CustomSetPagination

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        print(f"user : {user}")
        instance = self.get_object()
        print(f'instance = {instance.id}')
        serializer = self.get_serializer(instance)
        return_data = serializer.data
        return_data['status'] = 'success'
        return_data = serializer.get_server_filter(return_data)
        return Response(return_data)

    # def update(self, request, *args, **kwargs):

    @action(detail=False, methods=['POST'])
    def add_server(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['POST'],
            url_name="process-ml",
            url_path="process-ml",
            permission_classes=[AllowAny],
            )
    def processML(self, request):
        data = request.data
        model_data = [np.array(list(data.values()))]
        print(f"model_data: {model_data}")
        model_file = os.path.join(settings.BASE_DIR, 'User/MLmodel/model.pkl')
        print(f"Model file path: {model_file}")
        model = pickle.load(open(model_file, 'rb'))
        prediction = model.predict(model_data)
        output = round(prediction[0], 2)
        print(f"output : {output}")
        return Response(output, status=status.HTTP_200_OK)
