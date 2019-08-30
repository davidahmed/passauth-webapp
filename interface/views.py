from django.shortcuts import render
from django.template import loader


from django.http import HttpResponse


def index(request):
    template = loader.get_template('interface/index.html')
    return HttpResponse(template.render())

def consent(request):
    template = loader.get_template('interface/consent.html')
    return HttpResponse(template.render())
