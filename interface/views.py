from django.shortcuts import render
from django.template import loader


from django.http import HttpResponse


def index(request):
    template = loader.get_template('interface/index.html')
    return HttpResponse(template.render())

def consent(request):
    template = loader.get_template('interface/consent.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('interface/login.html')
    return HttpResponse(template.render())

def sorry(request):
    template = loader.get_template('interface/sorry.html')
    return HttpResponse(template.render())

def success(request):
    template = loader.get_template('interface/success.html')
    return HttpResponse(template.render())

def choices(request):
    template = loader.get_template('interface/choices.html')
    return render(request, 'interface/choices.html', {'images':['img/1.jpg', 'img/2.jpg']})
