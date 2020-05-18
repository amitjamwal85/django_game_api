from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def user_login(request):
    template = loader.get_template( 'login.html' )
    return HttpResponse( template.render( {}, request ) )


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required
def index(request):
    template = loader.get_template( 'index.html' )
    return HttpResponse( template.render( {}, request ) )


def login_action(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    user = authenticate( username=username, password=password )
    if user:
        if user.is_active:
            login( request, user )
            return HttpResponseRedirect( reverse( 'index' ) )
        else:
            return HttpResponse( "Your account was inactive." )
    else:
        print( "Someone tried to login and failed." )
        print( f"They used username: {username} and password: {password}" )
        return HttpResponse( "Invalid login details given" )