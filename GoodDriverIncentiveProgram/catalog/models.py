from django.db import models
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, reverse

class KeyWord(models.Model):
    word = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.word

class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    imgUrl = models.TextField(null=True)
    keyWord = models.ForeignKey(KeyWord, on_delete=models.CASCADE, default='')
    condition = models.CharField(max_length=100, default='')
    conditionId = models.IntegerField(default=0, null=True)
    slug = models.SlugField(max_length=2000, unique=False)

    def __str__(self):
        return self.title

    def getAddToCart(self):
        return reverse('catalog:addToCart', kwargs={'slug': self.slug})

    def getRemFromCart(self):
        return reverse('catalog:remFromCart', kwargs={'slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.item

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    startDate = models.DateTimeField(auto_now_add=True)
    orderDate = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
