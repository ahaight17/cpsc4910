from django.conf.urls import url, include
from django.urls import path, include
from GoodDriverIncentive import views
from django.contrib.auth import views as auth_views

#Setting the namespace
app_name = 'GoodDriverIncentive'


urlpatterns = [
    #url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    #url(r'^user/(?P<pk>\d+)/', views.DriverList.as_view(), name='your_drivers'),
    url(r'^user/(?P<pk>\d+)/', views.get_drivers, name='your_drivers'),
    url(r'^balance/(?P<pk>\d+)/', views.balance, name='balance')
]
