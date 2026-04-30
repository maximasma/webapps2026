"""
URL configuration for webapps2026 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views

import webapps2026
from register import views as register_views
from payapp import views as payapp_views
from api import views as api_views

# all urls
urlpatterns = [

    path('', register_views.index, name='index'),
    path('login/', register_views.Login, name='login'),
    path('logout/', register_views.logout_view, name='logout'),
    path('register', register_views.register, name='register'),

    path('send_money', payapp_views.send_money, name='send_money'),
    path('past_transactions', payapp_views.past_transactions, name='past_transactions'),
    path('request_money', payapp_views.request_money, name='request_money'),
    path('user_requests', payapp_views.user_requests, name='user_requests'),
    path('admin_transactions', payapp_views.admin_transactions, name='admin_transactions'),
    path('admin_accounts', payapp_views.admin_accounts, name='admin_accounts'),

    path('exchange/<str:currency1>/<str:currency2>/<str:amount>', api_views.exchange, name='exchange'),
    path('initial_exchange/<str:currency>', api_views.initial_exchange, name='initial_exchange'),
]
