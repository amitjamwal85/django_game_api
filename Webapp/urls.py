from django.urls import path
from Webapp import views

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('login.action/', views.login_action, name='login_action'),
    path('index/', views.index, name='index'),

    path('celery_task/', views.celery_task, name='celery_task'),

    path('posts/', views.detail, name='posts'),
    path('posts/<slug:slug>', views.slug_detail, name='slug_detail')
]