# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.conf import settings
from django.forms import ValidationError
from django.contrib.auth.decorators import login_required
import stripe

def home(request):
    params = {}
    params['home'] = True 
    return render_to_response('pages/index.html', params)

def about(request):
    params = {}
    params['about'] = True
    return render_to_response('pages/about.html', params); 

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
                    ['info@sivams.com'], fail_silently=False)
        except ValidationError:
            params['name'] = name;
            params['email'] = email;
            params['body'] = body;
            params['form_email_failure'] = True;
    return render_to_response('pages/contact.html', params); 

@login_required
def client_charge(request):
    params={'settings':settings};
    params.update(csrf(request))
    if request.user.is_authenticated() and request.user.is_staff:
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')
        customer = request.POST.get('customer')

        if token:
            try:
                stripe.api_key = settings.STRIPE_SECRET_KEY_LIVE
                # create the charge on Stripe's servers - this will charge the user's card
                charge = stripe.Charge.create(
                        amount=int(float(amount)*100), # amount in cents, again
                        currency="usd",
                        card=token,
                        description=customer
                        )
                params['charge']  = True 
                params['amount'] = amount
                params['customer'] = customer 
            except Exception, e:
                params['error'] = str(e);
                

        params['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY_LIVE
        return render_to_response('pages/charge.html', params) 
    else:
        return HttpResponseRedirect('/') 

from admin_tools.dashboard import modules, Dashboard


