from django.conf.urls import include, url
from django.contrib import admin
from map import views
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
