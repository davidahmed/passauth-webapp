from collections import OrderedDict
import json
import random
import datetime

from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from . import users

from django.http import HttpResponse

images = ["img/"+str(i)+'_tn.jpg' for i in range(1, 17)]

user_ids = ['LYPJ', 'BMQG', 'IRYH', 'WOLI', 'TLVP', 'UFNY', 'PQEF', 'VEKE', 'LNHE', 'GKAS']

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
def before_login(request):
    if request.GET.get('userid', '').upper() in user_ids:
        request.session['userid'] = request.GET.get('userid', '').upper()
        request.session.modified = True
        return redirect('login')
    if request.session.get('userid', '').upper() in user_ids:
        return redirect('login')
    template = loader.get_template('interface/before_login.html')
    return HttpResponse(template.render())

@csrf_exempt
def login(request):
    user_id = request.session.get('userid', '')
    if user_id not in user_ids:
        return redirect('before_login')

    if is_mobile(request):
        return redirect('/')

    if request.POST:
        usernameLogs = json.loads(request.POST.get('usernameLogs',"[]"))
        passwordLogs = json.loads(request.POST.get('passwordLogs', "[]"))
        mouseLogs = json.loads(request.POST.get('mouseLogs',"[]")),
        mouseMeta = json.loads(request.POST.get('mouseMeta', "[]")),

        if len(mouseLogs) == 0 or len(passwordLogs) == 0:
            return render(request, 'interface/login.html', {'not_clicked': True})

        username = request.POST.get('un', '').lower()
        password = request.POST.get('passwordValue', '')

        if len(usernameLogs) < len(username) or len(passwordLogs) < len(password):
            return render(request, 'interface/login.html', {'not_clicked': True})

        print(username, password)

        #if users.authenticate(username, password):
        if username == 'dave' and password == 'dave':
            if users.put_user_logs(username, {
                'username': username,
                'u': user_id,
                'p': request.POST.get('passwordValue', ''),
                'server_time': datetime.datetime.now(),
                'session': users.get_user_session(user_id),
                'usernameLogs': usernameLogs,
                'passwordLogs': passwordLogs,
                'mouseLogs': mouseLogs,
                'mouseMeta': mouseMeta,
                'headers': request.headers,
            }):
                sessionCount = users.get_user_session(user_id, increment=True)
                #sessionCount = request.session.get('session_count', 0)
            assert sessionCount > 0, 'Fatal: session is not incrementing'
            spk = users.user_md5(username) if sessionCount >= 25 else ""
            random.shuffle(images)

            request.session['username'] = username
            request.session['userid'] = user_id
            request.session['session_count'] = sessionCount
            request.session['spk'] = spk
            request.session['nonce'] = users.id_generator()
            request.session.modified = True

            print(request.session)

            return redirect('choices' )

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

def message(request):
    template = loader.get_template('interface/message.html')
    return HttpResponse(template.render())

def choices(request):
    random.shuffle(images)
    params = {'images': images[0:6],
              'username': request.session.get('userid', ""),
              'session_count': request.session.get('session_count', ""),
              'spk': request.session.get('spk'),
              'images': images[0:6]}
    return render(request, 'interface/choices.html', params)


