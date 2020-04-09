from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('before_login', views.before_login, name='before_login'),
    path('consent', views.consent, name='consent'),
    path('login', views.login, name='login'),
    path('signup', views.message, name='signup'),
    path('choices', views.choices, name='choices'),
    path('sorry', views.sorry, name='sorry'),
    path('success', views.success, name='success'),
    path('message', views.message, name='message')

]
