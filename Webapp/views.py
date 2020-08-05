from django.shortcuts import render
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import os
from django.contrib import messages
import json

from django.views.decorators.csrf import csrf_exempt

from DjangoDRF import settings
from Webapp.models import  Posts
from Webapp.tasks import sleepy
from Webapp.util import extract_parameters

ERR_BAD_PARAM = 400


@csrf_exempt
def register_web(request):
    try:
        print(f"settings.TESTING : {settings.TESTING}")
        required = 'firstName', 'lastName', 'instrument', 'email', 'password', 'type'
        optional = 'imageUrl', 'facebookId', 'language'
        try:
            values = extract_parameters(json.loads(request.body), required, optional)
            print(f"values : {values}")
        except KeyError:
            return HttpResponse(status=ERR_BAD_PARAM)
        return HttpResponse('success')
    except Exception as e:
        print(e)


def celery_task(request):
    template = loader.get_template( 'celery.html' )
    sleepy.delay(10)
    messages.success(request, 'We are processing request wait for some time.' )
    return HttpResponse( template.render( {}, request ) )


def user_login(request):
    template = loader.get_template( 'login.html' )
    return HttpResponse( template.render( {}, request ) )


def showcertfile(request, key):
    BASE_DIR = os.path.dirname(os.path.dirname( os.path.abspath( __file__ ) ) )
    wf_filepath = f'{BASE_DIR}/well-known/pki-validation/{key}'
    if os.path.exists(wf_filepath):
        with open(wf_filepath, 'rb') as fh:
            return HttpResponse(fh.read())


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





def detail(request):
    posts = Posts.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'slug/details.html', context )


def slug_detail(request, slug):
    q = Posts.objects.filter(slug__iexact=slug)
    if q.exists():
        q = q.first()
    else:
        raise Http404("Page not found")
    context = {
        'post': q
    }
    return render(request, 'slug/view_slug.html', context )