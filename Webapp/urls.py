

from django.urls import path
from Webapp import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('login.action/', views.login_action, name='login_action'),
    path('index/', views.index, name='index'),
]