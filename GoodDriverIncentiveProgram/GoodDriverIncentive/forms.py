from django import forms
from GoodDriverIncentive.models import User, Driver, Sponsor
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username', 'password', 'email')



# class UserProfileInfoForm(forms.ModelForm):
#     class Meta():
#         model = UserProfileInfo
#         fields = ('portfolio_site', 'profile_pic')

#class RegistrationForm(UserCreationForm):
#    email = forms.EmailField(required = True)

#    class Meta:
#        model = User
#        fields = (
#            'first_name',
#            'last_name',
#            'email',
#            'password1',
#            'password2'
#        )

#        def save(self, commit = True):
#            user = super(RegistrationForm, self).save(commit = False)
#            user.firstName = self.cleaned_data['firstName']
#            user.lastName = self.cleaned_data['lastName']
#            user.email = self.cleaned_data['email']

#            if commit:
#                user.save

#            return user

class DriverSignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

        def save(self, commit = True):
            user = super().save(commit = False)
            user.is_driver = True
            user.save()
            user.firstName = self.cleaned_data['firstName']
            user.lastName = self.cleaned_data['lastName']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            #group = Group.objects.get(name='Drivers')
            #user.group.add(group)

            #driver = Driver.objects.create(user=user)
            #driver.save()

            if commit:
                user.save()

            return user

class SponsorSignUpForm(UserCreationForm):
    email = forms.EmailField(required = True)
    drivers = forms.ModelMultipleChoiceField(
        queryset = User.objects.filter(groups__name='Drivers'),
        widget = forms.CheckboxSelectMultiple,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2'
        )

        @transaction.atomic
        def save(self, commit=True):
            user = super().save(commit=False)
            user.is_sponsor = True
            

            user.firstName = self.cleaned_data['firstName']
            user.lastName = self.cleaned_data['lastName']
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['username']
            sponsor = Sponsor.objects.create(user=user)
            sponsor.drivers.add(*self.cleaned_data.get('drivers'))

            #group = Group.objects.get(name='Sponsors')
            #user.group.add(group)

            if commit:
                user.save()
            return user
