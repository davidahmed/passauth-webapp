from collections import OrderedDict
import json
import random

from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .db import MongoDBConnection
from . import users

from django.http import HttpResponse

images = ["img/"+str(i)+'_tn.jpg' for i in range(1, 17)]
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

        if users.user_exists(request.POST.get('un', "")):
            return redirect('choices')
        else:
            return render(request, 'interface/login.html', {'login_error':True})
    return render(request, 'interface/login.html')

@csrf_exempt
def signup(request):
    if request.POST:
        username = request.POST.get('un', '')
        password = request.POST.get('pass', '')
        passwordConfirm = request.POST.get('passConfirm', '')

        if not (len(username) and len(password) and len(passwordConfirm)):
            return render(request, 'interface/signup.html', {'signup_error': "Come on! you can't leave a field blank"})
        if not password == passwordConfirm:
            return render(request, 'interface/signup.html', {'signup_error': "Passwords don't match"})
        if users.user_exists(request.POST.get('un', "")):
            return render(request, 'interface/signup.html', {'signup_error':'Someone already took that username'})
        else:
            validation = users.validate_signup(username, password)
            if validation[0] == False:
                return render(request, 'interface/signup.html', {'signup_error':validation[1]})
            else:
                return render(request, 'interface/signup.html', {'signup_valid': True})

    return render(request, 'interface/signup.html')

def sorry(request):
    template = loader.get_template('interface/sorry.html')
    return HttpResponse(template.render())

def success(request):
    template = loader.get_template('interface/success.html')
    return HttpResponse(template.render())

def choices(request):
    template = loader.get_template('interface/choices.html')
    random.shuffle(images)
    return render(request, 'interface/choices.html', {'images':images[0:6]})


