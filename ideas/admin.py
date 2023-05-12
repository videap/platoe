from django.contrib import admin
from ideas.models import *

class RequestAdmin(admin.TabularInline):
    model = Request

class IdeaAdmin(admin.TabularInline):
    model = Idea

class StripeAdmin(admin.TabularInline):
    model = Stripe_Account

class UserAdm(admin.ModelAdmin):
   inlines = [StripeAdmin, RequestAdmin, IdeaAdmin]

class RequestAdm(admin.ModelAdmin):
   inlines = [IdeaAdmin]


# Register your models here.

admin.site.register(User, UserAdm)
admin.site.register(Request, RequestAdm)
admin.site.register(Idea)
admin.site.register(Shared_Idea)
admin.site.register(Rating)
admin.site.register(Stripe_Account)
admin.site.register(Payment_Intent)

