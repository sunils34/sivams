# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.conf import settings
from django.contrib.auth.decorators import login_required
import stripe

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
                stripe.api_key = settings.STRIPE_SECRET_KEY_TEST
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
                

        params['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY_TEST
        return render_to_response('pages/charge.html', params) 
    else:
        return HttpResponseRedirect('/') 
