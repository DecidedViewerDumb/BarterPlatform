from django.shortcuts import render


def index(request):
    return render(request, 'forms/index.html')


def register(request):
    return render(request, 'forms/register.html')
