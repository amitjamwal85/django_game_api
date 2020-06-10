from django.contrib.auth.models import User
from rest_framework.schemas import AutoSchema
import coreschema, coreapi
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.authtoken.models import Token
from Games.models import Games, ContactUs
from Games.serializers import GameSerializer, LoginSerializer, ContactUsSerializer, AddS3FileSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from User.utils import IsAuthenticated

# from rest_framework_simplejwt.tokens import RefreshToken
# from six import text_type


class GameView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = GameSerializer
    queryset = Games.objects.all()
    lookup_field = 'pk'

    def list(self, request, *args, **kwargs):
        action_games = self.queryset.filter( category='action' )[:4]
        sports_games = self.queryset.filter( category='sports' )[:4]
        racing_games = self.queryset.filter( category='racing' )[:4]
        serializer_action = self.get_serializer( action_games, many=True )
        serializer_sports = self.get_serializer( sports_games, many=True )
        serializer_racing = self.get_serializer( racing_games, many=True )
        data = dict()
        data['action'] = serializer_action.data
        data['sports'] = serializer_sports.data
        data['racing'] = serializer_racing.data
        return Response( data )


    @action(
        methods=["post", "get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="adds3file",
        url_name="adds3file",
        serializer_class=AddS3FileSerializer,
    )
    def adds3file(self, request):
        if request.method == "POST":
            serializer = AddS3FileSerializer(data=request.data)
            if serializer.is_valid( raise_exception=True ):
                validated_data = serializer.validated_data
                s3file = serializer.create(validated_data=validated_data)
                return Response(
                    {"status": f'{s3file.file.url}'},
                    status=status.HTTP_201_CREATED,
                )

        if request.method == "GET":
            serializer = AddS3FileSerializer(request.user)
            data = serializer.get_allfiles()
            return_data = dict()
            return_data['S3URL'] = data
            return Response(return_data, status=status.HTTP_200_OK )


class LoginView(APIView):
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                name="username",
                required=True,
                # location="query",
                location="body",
                schema=coreschema.String(description="Username is required"),
            ),
            coreapi.Field(
                name="password",
                required=True,
                # location="query",
                location="body",
                schema=coreschema.Enum(
                    ("users", "songs", "trending", "notifications", "lyrics")
                )
            ),
        ]
    )

    def post(self, request):
        data = request.data
        print("data:", data)
        serializer = LoginSerializer( data=data )
        if serializer.is_valid( raise_exception=True ):
            username = serializer.data.get( "username" )
            password = serializer.data.get( "password" )
            print( f"{username}#{password}" )
            user = authenticate( username=username, password=password )
            # token = RefreshToken.for_user( user )
            # print( f"{text_type(token.access_token)} # {text_type(token)}" )
            if not user:
                return Response( {'error': 'Invalid Credentials'},
                                 status=HTTP_404_NOT_FOUND )

            user_data = User.objects.get(username=user)
            resp_data = dict()
            resp_data['email'] = user_data.email
            resp_data['username'] = user_data.username
            token, _ = Token.objects.get_or_create( user=user )
            resp_data['token'] = token.key
            return Response( resp_data,
                             status=HTTP_200_OK )



class ContactUsView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = ContactUsSerializer
    queryset = ContactUs.objects.all()
    lookup_field = "pk"