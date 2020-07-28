from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from DjangoDRF import schema
from Games.view import GameView, ContactUsView, LoginView
from User.view import TokenObtainPairView, TokenRefreshView, UserAPIView, ServerView, UserViewSet, PostView
from rest_framework.documentation import include_docs_urls
from graphene_django.views import GraphQLView
# from rest_framework_simplejwt import views as jwt_views
from Webapp import views
# from ESearch import views as search_view

login = TokenObtainPairView.as_view()
refresh = TokenRefreshView.as_view()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('webapp/', include('Webapp.urls')),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    # path('publisher/', include('ESearch.urls')),

    path('game/login/', LoginView.as_view(), name="game-login"),
    # path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

    url('^docs/', include_docs_urls(title='Django DRF', permission_classes=[AllowAny])),
    path('api/token/', login, name="user-login"),
    path('api/token/refresh/', refresh, name='token_refresh'),
    path( "graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),

    # path('search', search_view.search, name='search'),
    path('well-known/pki-validation/<str:key>', views.showcertfile, name='showcertfile'),
    path('chat/', include('justchat.urls')),
]

router = routers.SimpleRouter()
router.register(r'users', UserAPIView)
# router.register(r'users', UserViewSet, basename='user')
router.register(r'server', ServerView)
router.register(r'post', PostView)
router.register(r'game', GameView)
router.register(r'contact', ContactUsView)
urlpatterns += router.urls