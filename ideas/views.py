from datetime import datetime, timezone, timedelta

from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.contrib.auth import authenticate, login, logout, password_validation
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
from django.core.exceptions import ValidationError
from django.shortcuts import render

from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt

from ideas.models import *
from ideas.functions import *
from ideas.api_stripe import *
#index page
def index(request):
    return render(request, "index.html")

#login view
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]


        #if user exists, check if it is blocked.
        try:
            user = User.objects.get(username=username)
            if user.failed_logins >=5: #User gets blocked if more than 5 attempts
                blocked = True
            else: 
                blocked = False
        

            #Check if user is not trying to bruteforce, and register login attempt
            if blocked:
                time_difference = datetime.now(timezone.utc) - user.last_login_attempt
                user.last_login_attempt = datetime.now(timezone.utc)

                if time_difference.total_seconds() <=30: # if user has not waited 10min (600s) for next attempt TODO change time for waiting
                    user.save()
                    return render(request, "login.html", {
                        "message": "Too many requests. Try again later."
                        })
                else: #user has waited 10 min
                    user.failed_logins = 0
                    user.save()
        except:
            pass
        
        #try to authenticate
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            user.failed_logins = 0
            user.save()
            login(request, user)    
            return HttpResponseRedirect(reverse("index"))

        else:
            try:
                #if user exists, compute a failed login
                user = User.objects.get(username=username)
                user.failed_logins += 1
                user.last_login_attempt = datetime.now(timezone.utc)
                user.save()
            except:
                pass
                
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register_view(request):
    if request.method == "POST":
        validation = validate_new_user(request)

        if validation["message"] == "Database Updated":
            return HttpResponseRedirect(reverse("paymentinfo"))

        return render(request, "register.html", {
                "message": validation["message"],
                "pwd_message": validation["pwd_message"],
            })

    else:
        return render(request, "register.html")

@login_required
def myaccount(request):
    user_info = User.objects.get(id=request.user.id)
    user_info.birthdate = user_info.birthdate.strftime('%Y-%m-%d')
    if request.method == "POST":
        validation = update_user(request)

        if validation["message"] == "Database Updated":
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "myaccount.html", {
                "user_info": user_info,
                "message": validation["message"],
            })
    else:

        return render(request, "myaccount.html", {
            "user_info": user_info
        })

@login_required
def change_password_view(request):
    if request.method == "POST":
        #Authenticate old password:
        message = False
        pwd_message = False
        username = request.user.username
        old_password = request.POST["old_password"]
        user = authenticate(username=username, password=old_password)
        if user is None:
            #not authenticated
            message = "Old password is incorrect."
        else:
            #authenticated
            #Ensure password matches confirmation
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            if password != confirmation:
                message = "Passwords must match."
            else:
                try:
                    password_validation.validate_password(password)
                    user.set_password(password)
                    user.save()
                    login(request, user)
                    return HttpResponseRedirect(reverse("myaccount"))
                except ValidationError as valid_err:
                    pwd_message = valid_err

        return render(request, "changepassword.html", {
            "message": message,
            "pwd_message": pwd_message
        })

            
    else:
        return render(request, "changepassword.html")

def reset_password_view(request):
    #user is changing password
    if request.method == "POST":
        try:
            user= User.objects.get(email=request.POST["email"])
            message = "User found."
        except User.DoesNotExist as err:
            message = err
            return render(request, "reset_password.html",{
                "message": message,
            })

        #SEND EMAIL STEPS: TO BE CONFIGURED
        try:
            # subject="Password Change"
            # content="To change your email password, click on the link below."
            # send_mail(subject, content, "admin@example.com",(user.email,))
            # message = "A link to change your password was sent to your email."
            #TODO: Actually send email with mail server.

            #Create Hash Link
            hash = change_password_hash(user.username)

        except BadHeaderError:
            message = "Bad Header Error. Please, try again."

        return render(request, "reset_password.html",{
                "message": message,
                "hash": hash
            })

    else:
        return render(request, "reset_password.html")


def reset_password_hash(request, hash):

    #decode hash and get username and timestamp of email
    string = unhash_data(hash)
    array = string_to_array(string)

    # check if hash is a valid one
    if array[0].decode('UTF-8') == "valid_hash":
        timestamp = datetime.strptime(array[1].decode('UTF-8'), "%m/%d/%Y %H:%M:%S")
        user = User.objects.get(username=array[2].decode('UTF-8'))

        if timestamp < (datetime.now() - timedelta(hours=24)): #link should expire in 24h
            return HttpResponse("The link has expired")
    else:
        return HttpResponse(f"This link is invalid.")

    if request.method == "POST":
        #Authenticate old password:
        message = False
        pwd_message = False
        username = user.username
        
        #Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            message = "Passwords must match."
        else:
            try:
                password_validation.validate_password(password)
                user.set_password(password)
                user.save()
                login(request, user)
                return HttpResponseRedirect(reverse("myaccount"))
            except ValidationError as valid_err:
                pwd_message = valid_err

        return render(request, "changepasswordhash.html", {
            "message": message,
            "pwd_message": pwd_message,
            "hash": hash
        })
   
    else:
        return render(request, "changepasswordhash.html", {
            "hash": hash
        })
    
@login_required
def my_requests_view(request):
    return render(request, "my_requests.html", {
        "username": request.user.username
    })


@login_required
def my_ideas_view(request):
    return render(request, "my_ideas.html")


@login_required
def all_requests_view(request):
    return render(request, "all_requests.html")


@login_required
def ideas_shared_view(request):
    return render(request, "ideas_shared.html")

@login_required
@ensure_csrf_cookie
def request_view(request, request_id):
    try:
        requester_username = Request.objects.get(id=request_id).requester.username
    except:
        requester_username = None

    return render(request, "request.html", {
        "request_id": request_id,
        "requester_username": requester_username,
    })

@login_required
def idea_view(request, idea_id):

    try:
        request_title = Shared_Idea.objects.get(idea_shared_id=idea_id).request.title
        request_id = Shared_Idea.objects.get(idea_shared_id=idea_id).request.id
        shared=True
    except:
        request_id = Idea.objects.get(id=idea_id).idea_request.id
        return render(request, "request.html", {
          "request_id": request_id,
            "requester_username": Idea.objects.get(id=idea_id).idea_request.requester.username,
            "message": "This idea was not shared with you."
        })


    return render(request, "idea.html", {
        "idea_id": idea_id,
        "request_title": request_title,
        "request_id": request_id,
        "shared": shared,
    })

@login_required
def stripe_create_account(request):
    response = create_account(request.user.id)

    return HttpResponseRedirect(response.url)

@login_required
def stripe_create_intent(request, idea_id):
    
    payment_method=""

    try:
        payment_method = request.GET["payment_method"]
    except:
        pass

    response = create_payment_intent(idea_id, request.user.id, payment_method)

    return HttpResponse(response)

@csrf_exempt
def stripe_webhook(request):
    response = stripe_webhook_recieved(request)
    return response

#view to help developers
def showresponse(request):
    return HttpResponse(request)

@login_required
def paymentinfo_view(request):
    return render(request, "paymentinfo.html", {
        "banking_acceptance": User.objects.get(id=request.user.id).banking_accept,
        "payment_acceptance": User.objects.get(id=request.user.id).payment_accept,
        "onboard_completed": finished_onboarding(request.user.id)
    })

@login_required
def stripe_create_card(request):
    response = create_card(request.user.id)
    return HttpResponse(response)

@login_required
def stripe_update_account(request):
    url = update_account(request.user.id)
    return HttpResponseRedirect(url)

@login_required
def stripe_create_customer(request):
    response = create_customer(request)
    return HttpResponse(response)

@login_required
def stripe_list_cards(request):
    cards = list_cards(request.user.id)
    return JsonResponse(cards, safe=False, status=200)

@login_required
def stripe_detach_card(request, card_id):
    response = detach_card(card_id)
    if response:
        return JsonResponse({"OK": "Card Detached"}, status=200)
    else:
        return JsonResponse({"error": "Card not Detached"}, status=500)
