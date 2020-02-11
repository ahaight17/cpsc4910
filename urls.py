from django.conf.urls import url
from GoodDriverIncentive import views

#Setting the namespace
app_name = 'GoodDriverIncentive'

#urlpatterns = [
 #   path('signup/', views.SignUp.as_view(), name="signup")
#]

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
]