from GoodDriverIncentive.forms import UserForm, SponsorSignUpForm, DriverSignUpForm
#from GoodDriverIncentive.models import Sponsor, Driver
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, ListView, DetailView
from GoodDriverIncentive.decorators import driver_required, sponsor_required

from GoodDriverIncentive.models import User, Driver, Sponsor

class SignUpView(TemplateView):
    template_name = 'signup.html'

class DriverSignUpView(CreateView):
    context_object_name = 'is_driver'
    model = User
    form_class = DriverSignUpForm
    template_name = 'registration.html'
    
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Driver'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name='Drivers'))
        login(self.request, user)
        return HttpResponseRedirect(reverse('index'))


class SponsorSignUpView(CreateView):
    model = User
    form_class = SponsorSignUpForm
    template_name = 'registration.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Sponsor'
        return super().get_context_data(**kwargs)
    
    def form_valid(self, form):
        user = form.save()
        user.groups.add(Group.objects.get(name='Sponsors'))
        login(self.request, user)
        return HttpResponseRedirect(reverse('index'))

class DriverList(DetailView):
    model = User
    template_name = "sponsor_list.html"
    #pk_url_kwarg = "sponsor_id"
    slug_url_kwarg = 'drivers'
    #query_pk_and_slug = True
    

    #def get_queryset(self):
     #   return Sponsor.drivers.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['driver_list'] = User.objects.filter(groups__name='Drivers')

        return context

#def add_points(request, pk):
#    if request.method == 'POST':
#        user = User.objects.get(pk=pk)
#        user.points += 100
#        user.save()

def get_drivers(request, pk):
    users = User.objects.filter(groups__name='Drivers')
    context = {
        'users': users
    }
    return render(request, "sponsor_list.html", context)

def balance(request, pk):
    user = User.objects.get(pk=pk)
    msg=""
    if request.method == "POST":
        try:
            #username = request.POST["username"]
            amount = request.POST["amount"]
            #senderUser = User.objects.get(username=request.user.username)
            #receiverUser = User.objects.get(username=username)
            #user = User.objects.get(username = username)
            user.points = user.points + int(amount)
            user.save()
            msg = f"{amount} Points successfully added"
        except Exception as e:
            print(e)
            msg = "Points were not added. Please try again"
    #user = User.objects.get(pk=request.user)
    return render(request, 'points_add.html', {"msg":msg})


def index(request):
    return render(request, 'index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegistrationForm(data=request.POST)
        if user_form.is_valid():
            user_form.save()
            return render(request, 'index.html')
        else:
            print(user_form.errors)
    else:
        user_form = RegistrationForm()
    return render(request, 'registration.html',
                            {'user_form': user_form,
                             'registered': registered})

#def register(request):
#    registered = False
#    if request.method == 'POST':
#        user_form = RegistrationForm(data=request.POST)
#        if user_form.is_valid():
#            user_form.save()
#            return render(request, 'index.html')
#        else:
#            print(user_form.errors)
#    else:
#        user_form = RegistrationForm()
#    return render(request, 'registration.html',
#                            {'user_form': user_form,
#                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return render(request, 'login.html',
                            {'login_message' : 'Sorry, we couldn\'t find an account with that username and password.'})
    else:
        return render(request, 'login.html', {})

