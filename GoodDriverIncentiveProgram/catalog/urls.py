from catalog import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

#Setting the namespace
app_name = 'catalog'

#urlpatterns = [
 #   path('signup/', views.SignUp.as_view(), name="signup")
#]

urlpatterns = [
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^finish-checkout/$', views.checkout, name='checkout'),
    url(r'^addWords/$', views.addWords, name='addWords'),
    url(r'^process-new-shipping/$', views.processNewShipping, name='processNewShipping'),
    url(r'^checkout/$', views.checkoutPage, name='checkoutPage'), 
    url(r'^cancel-order/(?P<pk>\d+)/$', views.cancelOrder, name='cancelOrder'), 
    url(r'^change-shipping-address/(?P<pk>\d+)/$', views.changeShipping, name='changeShipping'),
    url(r'^past-orders/$', views.pastOrders, name='pastOrders'),
    url(r'^deleteWords/$', views.deleteWords, name='deleteWords'),
    url(r'^(?P<slug>[\w-]+)/$', views.prodDetail, name='prodDetail'),
    url(r'^add-to-cart/(?P<slug>[\w-]+)/$', views.addToCart, name='addToCart'),
    url(r'^remove-from-cart/(?P<slug>[\w-]+)/$', views.remFromCart, name='remFromCart'),   
]