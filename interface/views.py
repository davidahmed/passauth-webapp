from collections import OrderedDict
import json
import random

from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from bson.binary import Binary

from .db import MongoDBConnection
from . import users

from django.http import HttpResponse

images = ["img/"+str(i)+'_tn.jpg' for i in range(1, 17)]

def is_mobile(request):
    if request.user_agent.is_mobile or \
        request.user_agent.is_tablet or \
        request.user_agent.is_touch_capable:
        return True
    return False

def index(request):
    if is_mobile(request):
        return render(request, 'interface/index.html', {'is_mobile': True})

    template = loader.get_template('interface/index.html')
    return HttpResponse(template.render())

def consent(request):
    if request.session.get('consent', False):
        request.session['consent'] = True
        return redirect('login')


    template = loader.get_template('interface/consent.html')
    return HttpResponse(template.render())

@csrf_exempt
def login(request):
    if is_mobile(request):
        return redirect('/')
    if request.POST:
        usernameLogs = json.loads(request.POST.get('usernameLogs',"[]"))
        passwordLogs = json.loads(request.POST.get('passwordLogs', "[]"))
        mouseLogs = json.loads(request.POST.get('mouseLogs',"[]"))

        username = request.POST.get('un', '').lower()

        if users.authenticate(username, request.POST.get('pass',"")):
            if users.put_user_logs(username, {
                'u': username,
                'p': request.POST.get('pass', ''),
                'session': users.get_user_session(username),
                'usernameLogs': usernameLogs,
                'passwordLogs': passwordLogs,
                'mouseLogs': mouseLogs,
                'headers': request.headers,
            }):
                sessionCount = users.get_user_session(username, increment=True)
            assert sessionCount > 0, 'Fatal: session is not incrementing'
            spk = users.user_md5(username) if sessionCount >= 20 else ""
            random.shuffle(images)
            return render(request, 'interface/choices.html', {'username': username,
                                                                'session_count': sessionCount,
                                                                'spk': spk,
                                                                'images': images[0:6]})
        else:
            return render(request, 'interface/login.html', {'login_error':True})
    return render(request, 'interface/login.html')

@csrf_exempt
def signup(request):
    if request.POST:
        username = request.POST.get('un', '').lower()
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
                users.register_user(username, password)
                return render(request, 'interface/signup.html', {'signup_valid': True})

    return render(request, 'interface/signup.html' )

def sorry(request):
    template = loader.get_template('interface/sorry.html')
    return HttpResponse(template.render())

def success(request):
    template = loader.get_template('interface/success.html')
    return HttpResponse(template.render())

def choices(request):
    random.shuffle(images)
    return render(request, 'interface/choices.html', {'images':images[0:6]})


