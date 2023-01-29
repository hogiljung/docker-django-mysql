"""servertest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.template.defaulttags import url
from rest_framework import routers
from django.urls import include, re_path, path

import test.views
import sign.views
import board.views

router = routers.DefaultRouter()
#router.register(r'users', login.views.UserView, basename='users')
#router.register(r'signup', signup.views.signup, basename='signup')
router.register(r'users', sign.views.SignView, basename='users')
router.register(r'posts', board.views.PostView, basename='postlist')
urlpatterns = [
    re_path(r'^',include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', sign.views.SignView.signup),
    path('signin/', sign.views.SignView.signin),
    path('post/', board.views.PostView.postContentView),
    path('delete/', board.views.PostView.deleteContentView),
    path('modify/', board.views.PostView.modifyContentView),
    path('titleview/',board.views.PostView.briefContentView),
    path('contentview/',board.views.PostView.contentView),
    path('checkauthorview/',board.views.PostView.checkAuthorView),
    #path('tests/', test.views.TestView.login),
]
