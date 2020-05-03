from django.db import models
from django.contrib.auth.models import AbstractUser
from GoodDriverIncentive.errors import InsufficientBalance
# Create your models here.

class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    is_sponsor = models.BooleanField(default=False)
    points = models.IntegerField(default=0)

class Driver(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    #points = models.

    def __str__(self):
        return self.user.username


class Sponsor(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    drivers = models.ManyToManyField(Driver)
