from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.authtoken.models import Token
from Games.models import Games, ContactUs
from Games.serializers import GameSerializer, LoginSerializer, ContactUsSerializer
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


class LoginView(APIView):

    def post(self, request):
        data = request.data
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