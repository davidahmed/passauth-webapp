from collections import OrderedDict
import json
import random

from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

images = ["img/"+str(i)+'.jpg' for i in range(1, 17)]
def index(request):
    template = loader.get_template('interface/index.html')
    return HttpResponse(template.render())

def consent(request):
    if request.session.get('consent', False):
        return redirect('login')
    request.session['consent'] = True

    template = loader.get_template('interface/consent.html')
    return HttpResponse(template.render())

@csrf_exempt
def login(request):
    if request.POST:
        print(list(request.POST.items()))
        print("____LOGS______")
        print(json.loads(request.POST.get('usernameLogs',"[]")))
        print(json.loads(request.POST.get('passwordLogs', "[]")))
        print(json.loads(request.POST.get('mouseLogs',"[]")))
        print(request.__dict__)
        #Also save raw logs as well.

        if request.POST.get('un', "") == 'dave':
            return redirect('success')
    return render(request, 'interface/login.html')

def sorry(request):
    template = loader.get_template('interface/sorry.html')
    return HttpResponse(template.render())

def success(request):
    template = loader.get_template('interface/success.html')
    return HttpResponse(template.render())

def choices(request):
    template = loader.get_template('interface/choices.html')
    print(images)
    return render(request, 'interface/choices.html', {'images':random.choices(images, k=6)})
