import random
import string
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from ideas.forms import *
from ideas.models import User
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import login, password_validation
from cryptography.fernet import Fernet


#Function to validate the update for user information
@login_required
def update_user(request):
    var = {}
    
    #Create a ModelForm with Post Data
    try:
        user = User.objects.get(id=request.user.id)
        Updated_User = UpdateUser_ModelForm(request.POST, request.FILES, instance=user)


        if Updated_User.is_valid():
            Updated_User.save()
            var["message"] = "Database Updated"
        else:
            var["message"] = Updated_User.errors

    except IntegrityError as err:
        var["message"] = err

    return var

#Function to validate the creation of a user
def validate_new_user(request):

     # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        var = {}
        var["pwd_message"] = False

        if password != confirmation:
            var["message"] = "Passwords must match."
        else:
            #Create a ModelForm with Post Data
            try:
                New_User = NewUser_ModelForm(request.POST, request.FILES)

                #Validate Model Form. If valid, save entry and login
                if New_User.is_valid():
                    password_validation.validate_password(password)

                    user = New_User.save()

                    Stripe_Account(account_owner_id=user.id).save()
                    login(request, user)

                    var["message"] = "Database Updated"
                else:
                    var["message"] = New_User.errors
                

            except IntegrityError as err:
                var["message"] = err
            except ValidationError as valid_err:
                var["pwd_message"] = valid_err
                var["message"] = False

        return var

#Function to paginate elements
def paginate(request, array):

    try:
        page = request.GET["page"]
    except:
        page=1

    items_per_page = 3
    p = Paginator(array, items_per_page)

    response = {
        "ids": p.page(page).object_list,
        "first_page": 1,
        "actual_page": page,
        "last_page": p.num_pages,
        "has_next": p.page(page).has_next(),
        "has_previous": p.page(page).has_previous(),
    }

    return response

#Function to create hashes to change password
def change_password_hash(username):
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    to_hash="valid_hash"+ ";"+ now + ";" + username
    hash = hash_data(to_hash)
    return hash.decode('UTF-8')

def hash_data(data):
    # key = Fernet.generate_key()  # store in a secure location
    key = b'3fSEWXb5GpZo857kHb1Ma7ulCMuD3qUwdl3cvNEdTgE='
    return encrypt(data.encode(), key)


def unhash_data(hash):
    key = b'3fSEWXb5GpZo857kHb1Ma7ulCMuD3qUwdl3cvNEdTgE='
    hash = bytes(hash, 'utf-8')
    return decrypt(hash, key).decode()

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    try:
        token = Fernet(key).decrypt(token)
    except: 
        token = b"Error. Invalid Hash"
    return token

def string_to_array(string):
    array = [i.encode('utf8') for i in string.split(';')]
    return array