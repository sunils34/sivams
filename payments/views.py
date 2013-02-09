# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime 
import stripe
import os 
from django_xhtml2pdf.utils import generate_pdf
from django.template import Context
from django.core.mail import EmailMessage

@login_required
def client_charge(request):
    params={'settings':settings};
    params.update(csrf(request))
    if request.user.is_authenticated() and request.user.is_staff:
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')
        customer = request.POST.get('customer')
        email = request.POST.get('email')
        name = request.POST.get('name')

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
                send_invoice(charge, customer, amount);
            except Exception, e:
                params['error'] = str(e);
        

        params['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY_TEST
        return render_to_response('pages/charge.html', params) 
    else:
        return HttpResponseRedirect('/') 

def send_invoice(charge, description, amount, email=None, name=None):
    last4 = charge['card']['last4']
    card_type = charge['card']['type']
    chid = charge['id'];
    fname = '/home/sunil/invoices/' + chid + ".pdf";
    f=open(fname, 'w'); 
    f = generate_invoice(chid, description, amount, card_type, last4, email, name, file_object=f)
    f.close(); 
    f=open(fname, 'r'); 
    email = EmailMessage('Billing Receipt from Siva Microbiological Solutions', 'Attached is your receipt charged by Siva Microbiological Solutions LLC. (sivams.com).', 'Siva Microbiological Solutions <info@sivams.com>',
                        ['', ''], ['sunils34@gmail.com', 'lakshmi@sivams.com'],
                                    headers = {'Reply-To': 'info@sivams.com'});

    email.attach(chid+".pdf", f.read(), "application/pdf");
    email.send(); 


@login_required
def invoice(request):
    resp = HttpResponse(content_type='application/pdf')
    result = generate_invoice("abcdefg", "This is an awesome project", "10.05", "Visa", "5490", "sunils34@gmail.com", "Sunil", file_object=resp)
    
    f=os.tmpfile(); 
    f = generate_invoice("abcdefg", "This is an awesome project", "10.05", "Visa", "5490", "sunils34@gmail.com", "Sunil", file_object=f)
    email = EmailMessage('Receipt from Siva MS', 'Attached is your receipt', 'info@sivams.com',
                        ['sunils34@gmail.com', ''], ['sunils34@gmail.com'],
                                    headers = {'Reply-To': 'info@sivams.com'});
    email.attach('hihihi.pdf', f.read(), 'application/pdf');
    email.send(); 

    return result

def generate_invoice(invoice_number, description, amount_paid, card_type, last4, email=None, name=None, file_object=None):
    params = {}; 
    if email is not None:
        params['to_contact_email'] = email; 
    if name is not None:
        params['to'] = name; 
    params['description'] = description
    params['invoice_number'] = invoice_number; 
    params['amount_paid'] = amount_paid; 
    params['card_number'] = "XXXXXXXXXXXX" + last4 
    params['card_type'] = card_type; 
    params['date'] = datetime.now(); 
    context = Context(params)
    result = generate_pdf('invoice/invoice.html', file_object=file_object, context=context)
    return result; 

