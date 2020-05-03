"""GDIP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url, include
from GoodDriverIncentive import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from GoodDriverIncentive.decorators import driver_required, sponsor_required

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^special/', views.special, name='special'),
    url(r'^GoodDriverIncentive/', include('GoodDriverIncentive.urls')),
    url(r'^catalog/', include('catalog.urls')),
    path('GoodDriverIncentive/', include('django.contrib.auth.urls')),
    path('GoodDriverIncentive/signup/', views.SignUpView.as_view(), name='signup'),
    path('GoodDriverIncentive/signup/driver/', views.DriverSignUpView.as_view(), name='driver_signup'),
    path('GoodDriverIncentive/signup/sponsor/', views.SponsorSignUpView.as_view(), name='sponsor_signup'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^settings/', include('settings.urls')),
    #url(r'^user/(?P<pk>\d+)/', views.DriverList.as_view(), name='your_drivers'),
]
