# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.conf import settings
from django.forms import ValidationError

def home(request):
    params = {}
    params['home'] = True 
    return render_to_response('pages/index.html', params)

def construction(request):
    params = {}
    params['construction'] = True 
    return render_to_response('pages/construction.html', params)

def about(request):
    params = {}
    params['about'] = True
    return render_to_response('pages/about.html', params); 

def services(request):
    params = {}
    params['services'] = True
    return render_to_response('pages/services.html', params); 

def publications(request):
    params = {}
    params['publications'] = True
    return render_to_response('pages/publications.html', params); 

def gallery(request):
    params = {}
    params['gallery'] = True
    return render_to_response('pages/gallery.html', params); 

def contact(request):
    params = {}
    params['contact'] = True
    params.update(csrf(request))
    name = request.POST.get('name')
    email = request.POST.get('email')
    body = request.POST.get('body')
    if name:
        try:
            validate_email(email)
            params['form_submit'] = True;
            send_mail('[SIVAMS FORM] Message Received', 
                    '''%s\n\nFrom: %s'''%(body, name) , email,
                    ['lakshmi@sivamicrobialsolutions.com', 'sunil@sivamicrobialsolutions.com'], fail_silently=False)
        except ValidationError:
            params['name'] = name;
            params['email'] = email;
            params['body'] = body;
            params['form_email_failure'] = True;
    return render_to_response('pages/contact.html', params); 


from admin_tools.dashboard import modules, Dashboard


