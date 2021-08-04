from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from model_utils import Choices

category_choices = [
    ("COM", 'Company'),
    ("PRO", 'Product'),
    ("SVC", 'Service'),
    ("ART", 'Art'),
    ("OBJ", 'Object'),
    ("MOV", 'Movie'),
    ("TXT", 'Text'),
    ("BOK", 'Book'),
    ("OTH", 'Other'),
]



class User(AbstractUser):
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(unique=True, blank=False,max_length=150)
    first_name = models.CharField(blank=False, max_length=24)
    last_name = models.CharField(blank=False, max_length=24)
    birthdate = models.DateField(blank=False)
    image = models.ImageField(upload_to='profile_images', blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True)
    failed_logins = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)
    banking_accept = models.BooleanField(default=False)
    banking_accept_time = models.DateTimeField(null=True, blank=True)
    payment_accept = models.BooleanField(default=False)
    payment_accept_time = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return f"{self.id}: {self.username}"

class Request(models.Model):

    CATEGORY = Choices(
    ("COM", 'Company'),
    ("PRO", 'Product'),
    ("SVC", 'Service'),
    ("ART", 'Art'),
    ("OBJ", 'Object'),
    ("MOV", 'Movie'),
    ("TXT", 'Text'),
    ("BOK", 'Book'),
    ("OTH", 'Other'),
    )

    DEFINITION = Choices(
    ("COM_NAME","Idea for a Company Name"),
    ("COM_SLOGAN","Idea for a Company Slogan"),
    ("COM_BM","Idea for a Business Model"),
    ("COM_ASSET","Idea for a Company Asset"),
    ("COM_EV","Idea for a Company Event"),
    ("PRO_TOY","Idea for a Toy"),
    ("PRO_HOUSE","Idea for a House Item"),
    ("PRO_GADGET","Idea for a Gadget"),
    ("PRO_TECH","Idea for a Technology"),
    ("PRO_FEATURE","Idea for a Feature"),
    ("SVC_NEW","Idea for a New Service"),
    ("ART_MUS","Idea for a Music"),
    ("ART_DRAW","Idea for a Drawing"),
    ("ART_DANCE","Idea for a Dance"),
    ("OBJ_PRESENT","Idea for a Present"),
    ("OBJ_DECORATION","Idea for a Decoration"),
    ("OBJ_INVENTION","Idea for an Invention"),
    ("MOV_TITLE","Idea for a Title"),
    ("MOV_SCRIPT","Idea for a Script"),
    ("MOV_CHAR","Idea for a Character"),
    ("MOV_SCENE","Idea for a Scene"),
    ("TXT_LYRIC","Idea for a Lyric"),
    ("TXT_SCRIPT","Idea for a Script"),
    ("TXT_CHARACTER","Idea for a Character"),
    ("TXT_LETTER","Idea for a Letter"),
    ("OTH","Idea for something else")
    )


    title = models.CharField(blank=False, max_length=72)
    category = models.CharField(blank=False, choices=CATEGORY, max_length=50)
    definition = models.CharField(blank=False, choices=DEFINITION, max_length=50)
    something_else = models.CharField(blank=True, max_length=72)
    goal = models.CharField(blank=False, max_length=292)
    restrictions = models.CharField(blank=True, max_length=2048) 
    context = models.CharField(blank=True, max_length=2048)
    offer_value = models.DecimalField(blank=False, max_digits=7, decimal_places=2)
    requester = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_requests")
    request_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

class Idea(models.Model):
    # is_requested = models.BooleanField(blank=False)
    idea_title = models.CharField(blank=True, max_length=72)
    idea_request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_ideas")
    idealist = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_ideas")
    # validations = LIST OF BOOLEAN FOR EACH RESTRICTION FOR THE IDEALIST TO ACKNOWLEDGE #TODO: Define how to validate the restrictions
    content =  models.CharField(blank=False, max_length=2048)
    attachments = models.FileField(upload_to='ideas_files', blank=True)
    share_value = models.DecimalField(blank=False, max_digits=7, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=5)
    status = models.CharField(blank=False, max_length=12, default="offered")

    def __str__(self):
        return f"{self.id}: {self.idea_title}"

class Shared_Idea(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="request_shared_ideas")
    idea_shared = models.ForeignKey(Idea, on_delete=models.CASCADE)
    displayed_time = models.DateTimeField(auto_now_add=True)
    shared_value = models.DecimalField(max_digits=7, decimal_places=2)
    site_fee = models.DecimalField(max_digits=7, decimal_places=2)
    transferred_value = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.id}: Idea Shared: {self.idea_shared}"

class Rating(models.Model):
    rated_shared_idea = models.ForeignKey(Shared_Idea, on_delete=models.CASCADE)
    rater = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_ratings")
    rating_timestamp = models.DateTimeField(auto_now_add=True)


class Stripe_Account(models.Model):
    account_owner = models.OneToOneField("User", on_delete=models.CASCADE, related_name="stripe_account")
    stripe_id = models.CharField(blank=True, default="", max_length=25)
    customer_id = models.CharField(blank=True, default="", max_length=25)


    def __str__(self):
        return f"{self.account_owner}"

class Payment_Intent(models.Model):
    idea = models.ForeignKey("Idea", on_delete=models.CASCADE, related_name="ide_payment_intents")
    payment_user =  models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_payment_intents")
    payment_intent_id = models.CharField(blank=False, unique=True, max_length=30)

    def __str__(self):
        return f"{self.payment_intent_id}"
