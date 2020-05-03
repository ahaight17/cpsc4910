from settings import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include


#Setting the namespace
app_name = 'settings'

urlpatterns = [
    url(r'^$', views.settingsIndex, name='settingsIndex'),
]
