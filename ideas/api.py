import json
from ideas.models import *
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from ideas.forms import NewRequest_ModelForm, NewIdea_ModelForm
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from ideas.functions import paginate
from django.urls import reverse
import time


def get_my_requests_ids(request):
    #return json with "ids", "error" or "[None]" if no ids
    if request.user.is_authenticated:
        requests_ids = list(Request.objects.filter(requester_id=request.user.id).order_by("-request_timestamp").values_list("id", flat=True))

        response = paginate(request, requests_ids)

        if len(requests_ids) == 0:
            return JsonResponse(response, status=204)

        return JsonResponse(response, status=200)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

@login_required
def get_my_ideas_ids(request):
    #return json with "ids", "error" or "null" if no ids
    if request.user.is_authenticated:
        ideas_ids = list(Idea.objects.filter(idealist_id=request.user.id).order_by("-timestamp").values_list("id", flat=True))
        response = paginate(request, ideas_ids)

        if len(ideas_ids) == 0:
            return JsonResponse(response, status=204)

        return JsonResponse(response, status=200)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

@login_required
def get_my_shared_ideas_ids(request):
    #return json with "ids", "error" or "null" if no ids
    if request.user.is_authenticated:
        shared_ideas_ids = list(Shared_Idea.objects.filter(request__requester_id=request.user.id).order_by("-request__request_timestamp").values_list("idea_shared_id", flat=True))
        response = paginate(request, shared_ideas_ids)

        if len(shared_ideas_ids) == 0:
            return JsonResponse(response, status=204)

        return JsonResponse(response, status=200)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def get_request(request, id):
    #return json with "ids", "error", or "message" if no-content
    if request.user.is_authenticated:
        r = list(Request.objects.filter(id=id).values())

        if r: #id contains information and the array is not empty
            r = r[0]
            r["requester_username"] = User.objects.get(id=r["requester_id"]).username

            ideas_count=list(Request.objects.filter(id=id).values_list("request_ideas", flat=True))

            r["offered_ideas_count"] = len(list(filter(None, Request.objects.filter(id=id).values_list("request_ideas", flat=True))))
            r["shared_ideas_count"] = len(list(filter(None, Request.objects.filter(id=id).values_list("request_shared_ideas", flat=True))))
            r["request_definition"] = Request.objects.get(id=id).DEFINITION[Request.objects.get(id=id).definition]
            r["request_category"] = Request.objects.get(id=id).CATEGORY[Request.objects.get(id=id).category]
            return JsonResponse(r, status=200) #Status OK
        else:
            return JsonResponse({"message": "No Content"}, status=204) #Status No Content

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def get_idea(request, id):
    #return json with "ids", "error", or "message" if no-content
    if request.user.is_authenticated:

        i = list(Idea.objects.filter(id=id).values())
        if i: #id contains information and the array is not empty
            i = i[0]

            # check if user is the idealist, so it is authorized to see the idea content
            if request.user.id == i["idealist_id"]:
                i["idea_request_title"] = Request.objects.get(id=i["idea_request_id"]).title
                i["idea_request_category"] = Request.objects.get(id=i["idea_request_id"]).CATEGORY[Request.objects.get(id=i["idea_request_id"]).category]
                i["idea_request_definition"] = Request.objects.get(id=i["idea_request_id"]).DEFINITION[Request.objects.get(id=i["idea_request_id"]).definition]
                i["idealist_username"] = Idea.objects.get(id=id).idealist.username
                i["idea_request_category"] = Idea.objects.get(id=id).idea_request.CATEGORY[Idea.objects.get(id=id).idea_request.category]
                return JsonResponse(i, status=200)

            #if user is not the idealist, check if this idea can be shared.
            else:
                #check if idea exists in Shared_Ideas table
                try:
                    shared_idea = Shared_Idea.objects.get(idea_shared=id)
                except Shared_Idea.DoesNotExist: #idea was not shared, send only preview information
                    return JsonResponse({"error": "Forbidden."}, status=403) #Status Forbidden

                #check if user is the user authorized on shared ideas:
                if shared_idea.request.requester_id == request.user.id:
                    i["idea_request_title"] = Request.objects.get(id=i["idea_request_id"]).title
                    i["idea_request_category"] = Request.objects.get(id=i["idea_request_id"]).CATEGORY[Request.objects.get(id=i["idea_request_id"]).category]
                    i["idea_request_definition"] = Request.objects.get(id=i["idea_request_id"]).DEFINITION[Request.objects.get(id=i["idea_request_id"]).definition]
                    i["idealist_username"] = Idea.objects.get(id=id).idealist.username
                    return JsonResponse(i, status=200)
    
            
        else:
            return JsonResponse({"Message": "No Content"}, status=204) #Status No Content

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def new_idea(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            #check if user has accepted terms on banking
            if User.objects.get(id=request.user.id).banking_accept:
                    

                data = request.POST.dict()
                data["idealist"] = request.user.id
                data["share_value"] = Request.objects.get(id=data["idea_request"]).offer_value
                new_idea = NewIdea_ModelForm(data)


                if new_idea.is_valid():
                    new_idea.save()
                    return JsonResponse({"OK": "New idea request saved."}, status=200) #Status OK
                else:
                    return JsonResponse({"error": new_idea.errors}, status=422) #Status Unprocessable Entity
            #User must accept terms
            else: 
                return JsonResponse({"error_accept": "To share ideas, accept the Terms of Usage and set your Banking Information"}, status=401) #Status Unprocessable Entity

        else:
            return JsonResponse({"error": "Must be a POST request."}, status=405) #Status Method Not Allowed

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def new_request(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            data = request.POST.dict()
            data["requester"] = request.user.id
            new_idea_request = NewRequest_ModelForm(data)


            if new_idea_request.is_valid():
                new_idea_request.save()
                return JsonResponse({"OK": "New idea request saved."}, status=200) #Status OK
            else:
                return JsonResponse({"error": new_idea_request.errors}, status=422) #Status Unprocessable Entity

        else:
            return JsonResponse({"error": "Must be a POST request."}, status=405) #Status Method Not Allowed

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def get_requests(request):
    #return json with "ids", "error" or "[None]" if no ids
    if request.user.is_authenticated:
        #TODO insert filters in page 
        # filters = request.GET.dict()
        # requests_ids = list(Request.objects.filter(**filters).values_list("id", flat=True))

        requests_ids = list(Request.objects.filter().order_by("-request_timestamp").values_list("id", flat=True))
        
        response = paginate(request, requests_ids)

        return JsonResponse(response, status=200)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def get_ideas_from_requests_ids(http_request, request_id):
    #return json with "ids", "error" or "[None]" if no ids of the requests of the ideas not paid/shared
    if http_request.user.is_authenticated:
        filters = http_request.GET.dict()
        offered_ideas_ids = list(Request.objects.get(id=request_id).request_ideas.values_list("id", flat=True))
        
        response = {
            "ids": offered_ideas_ids
        }
        return JsonResponse(response, status=200)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def get_idea_preview(request, id):
    #return json with "ids", "error", or "message" if no-content
    if request.user.is_authenticated:

        i = list(Idea.objects.filter(id=id).values("idealist__username", "share_value", "rating", "timestamp", "idea_request_id", "status"))
        if i: #id contains information and the array is not empty
            i = i[0]
            i["timestamp"] = i["timestamp"].strftime("%d/%m/%y")
            return JsonResponse(i, status=200)    
        else:
            return JsonResponse({"Message": "No Content"}, status=204) #Status No Content

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def share_idea(request_id, idea_id, shared_value, site_fee, transferred_value):
        try:
            Shared_Idea(request=request_id, idea_shared=idea_id, shared_value=shared_value, site_fee=site_fee, transferred_value=transferred_value).save()
        except Shared_Idea.IntegrityError as err:
            return JsonResponse({"status": "Error.Could not share idea"})

        JsonResponse({"status": "OK"})

def accept_banking(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        if user.banking_accept:
            return JsonResponse({"banking": "Already Accepted"}, status=200)
        else:
            user.banking_accept=True
            user.banking_accept_time = timezone.now()
            try:
                user.save()
                return JsonResponse({"banking": "Acceptance Submitted"}, status=200)
            except:
                return JsonResponse({"Error": "NOT Submitted"}, status=500)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized

def accept_payment(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        if user.payment_accept:
            return JsonResponse({"payment": "Already Accepted"}, status=200)
        else:
            user.payment_accept=True
            user.payment_accept_time = timezone.now()
            try:
                user.save()
                return JsonResponse({"payment": "Acceptance Submitted"}, status=200)
            except:
                return JsonResponse({"Error": "NOT Submitted"}, status=500)

    else: #user is not authenticated
        return JsonResponse({"error": "User must be authenticated."}, status=401) #Status Unauthorized


