from django.shortcuts import render
from django.http import HttpResponse


def settingsIndex(request):
    return HttpResponse("Hello, world. You're at the settings index.")

