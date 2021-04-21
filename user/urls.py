from django.conf.urls import url
from django.urls import path

from . import views
from captcha.views import captcha_refresh

app_name = 'user'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('index/', views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.logout, name = 'logout'),
    path('confirm/', views.user_confirm),
    path('forget/',views.forget_index),
    path('forget/index/',views.forget_index),
    path('forget/confirm/',views.forget_confirm),
    path('forget/change/',views.forget_change),
    url(r'^refresh/',captcha_refresh)
]