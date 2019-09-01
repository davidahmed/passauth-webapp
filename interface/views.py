from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse


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
    return render(request, 'interface/login.html')

def sorry(request):
    template = loader.get_template('interface/sorry.html')
    return HttpResponse(template.render())

def success(request):
    template = loader.get_template('interface/success.html')
    return HttpResponse(template.render())

def choices(request):
    template = loader.get_template('interface/choices.html')
    return render(request, 'interface/choices.html', {'images':['img/1.jpg', 'img/2.jpg']})
