import json
import stripe
from ideas.models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse


def create_account (user_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    user = User.objects.get(id=user_id)

    stripe_account = Stripe_Account.objects.get(account_owner_id=user_id)

    #validate if the stripe account for banking does not exist
    if stripe_account.stripe_id == "": 
        created_account = stripe.Account.create(
            type='express',
            #country = "" define as ISO 3166-1 alpha-2 country code
            email = user.email,
            business_type = "individual",
            individual = {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                # "phone": user.phone, TODO prefill phone to stripe                
            },
            business_profile = {
                "support_email": user.email,
                "url": "https://plato.io",
            },
            
            # default_currency = "" Three-letter ISO currency code,
            metadata = { "username": user.username, "plato_id": user.id }
        )

        stripe_account.stripe_id = created_account.id
        stripe_account.save()

        account_link = create_account_link(created_account.id)

    else:
        account_link = create_account_link(Stripe_Account.objects.get(account_owner_id=user_id).stripe_id)
    
    return account_link


        
    
def create_account_link(stripe_account_id):
    account_link = stripe.AccountLink.create(
        account=stripe_account_id,
        refresh_url='http://127.0.0.1:8000/stripe',
        return_url='http://127.0.0.1:8000/',
        type='account_onboarding',
    )

    return account_link

def create_payment_intent(idea_id, request_user_id, payment_method):

    #CHECK if user has accepted terms of usage
    if User.objects.get(id=request_user_id).payment_accept:
        pass
    else:
        response = JsonResponse({"error_accept": True})
        response.status_code = 401 #Forbidden
        return response

    stripe.api_key = settings.STRIPE_SECRET_KEY

    requester_customer_id = Stripe_Account.objects.get(account_owner_id=request_user_id).customer_id
    idea = Idea.objects.get(id=idea_id)
    share_value = int(idea.share_value*100)
    application_fee = int(share_value*settings.APP_FEE)

    if payment_method == "": #payment method not provided

        payment_intent = stripe.PaymentIntent.create(
            payment_method_types=['card'],
            customer=requester_customer_id,
            #setup_future_usage="on_session", #optional if save card is enabled
            amount=share_value,
            currency='usd',
            application_fee_amount=application_fee,
            transfer_data={
                'destination': idea.idealist.stripe_account.stripe_id,
            }
        )

    else: #payment_intent was provided
        payment_intent = stripe.PaymentIntent.create(
            payment_method=payment_method,
            customer=requester_customer_id,
            setup_future_usage="on_session",
            amount=share_value,
            currency='usd',
            application_fee_amount=application_fee,
            transfer_data={
                'destination': idea.idealist.stripe_account.stripe_id,
            }
        )

    Payment_Intent(idea_id=idea_id, payment_user_id=request_user_id, payment_intent_id=payment_intent.id).save()

    return JsonResponse(payment_intent)

def stripe_webhook_recieved(request):
    if request.method == "POST":

        stripe.api_key = settings.STRIPE_SECRET_KEY
        webhook_secret = settings.WEBHOOK_SECRET

        request_data = request.POST
        signature = request.META['HTTP_STRIPE_SIGNATURE']

        # Verify webhook signature and extract the event.
        # See https://stripe.com/docs/webhooks/signatures for more information.
        try:
            event = stripe.Webhook.construct_event(
                payload=request.body, sig_header=signature, secret=webhook_secret
            )
        except ValueError as e:
            # Invalid payload.
            return HttpResponse("Invalid Payload", status=402)
        except stripe.error.SignatureVerificationError as e:
            #  Invalid Signature.
            return HttpResponse("Invalid Signature", status=403)

        if event["type"] == "charge.succeeded":
            payment_intent = event["data"]["object"]
            fullfill = handle_successful_payment_intent(payment_intent)
            if fullfill:
                return HttpResponse({"success": True}, 200)
            else:
                return HttpResponse("Idea was not shared", status=401)  
        else:
            return HttpResponse(status=400)

    else: 
        return HttpResponse(status=400)

def handle_successful_payment_intent(payment_intent):
    intent = Payment_Intent.objects.get(payment_intent_id=payment_intent.payment_intent)
    
    idea_id = intent.idea.id
    request_id = intent.idea.idea_request.id
    shared_value = int(payment_intent.amount_captured)/100
    site_fee = int(payment_intent.application_fee_amount)/100
    transferred_value = shared_value - site_fee

    try:
        Shared_Idea(request_id=request_id, idea_shared_id=idea_id, site_fee=site_fee, transferred_value=transferred_value, shared_value=shared_value).save()
        intent.delete()
        idea = Idea.objects.get(id=idea_id)
        idea.status = "shared"
        idea.save()
        return True
    except:
        return False

@login_required
def create_customer(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    user_id = request.user.id
    user = User.objects.get(id=user_id)

    if user.stripe_account.customer_id == "":

        customer = stripe.Customer.create(
            description=f"username: {user.username}", 
            email=user.email,
            phone=user.phone,
        )

        stripe_account = Stripe_Account.objects.get(account_owner_id=user_id)
        stripe_account.customer_id = customer.id
        stripe_account.save()

    else:
        customer = stripe.Customer.retrieve(user.stripe_account.customer_id)

    return JsonResponse(customer, status=200)

def create_card(user_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer_id = Stripe_Account.objects.get(account_owner_id=user_id).customer_id

    intent = stripe.SetupIntent.create(
        customer=customer_id
    )

    return JsonResponse(intent)

def list_cards(user_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    customer_id = Stripe_Account.objects.get(account_owner_id=user_id).customer_id

    cards = stripe.PaymentMethod.list(
        customer=customer_id,
        type="card",
    )

    #create dict for cards, being (paymentmethod_id, last4)
    safe_cards = dict()
    i=0
    for card in cards:
        safe_cards[i] = {"card_id": card.id, "card_brand": card.card.brand, "card_last4":card.card.last4}
        i+=1
        
    
    return safe_cards

def update_account(user_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    stripe_id = Stripe_Account.objects.get(account_owner_id=user_id).stripe_id

    link = stripe.Account.create_login_link(stripe_id)

    return link.url

def detach_card(payment_method_id):

    stripe.api_key = settings.STRIPE_SECRET_KEY


    stripe.PaymentMethod.detach(payment_method_id)

    return True

def finished_onboarding(user_id):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    stripe_id = Stripe_Account.objects.get(account_owner_id=user_id).stripe_id

    charges_enabled = stripe.Account.retrieve(stripe_id).charges_enabled

    return charges_enabled