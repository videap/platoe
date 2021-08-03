from django.urls import path
from ideas import views, api, api_stripe

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("myaccount/", views.myaccount, name="myaccount"),
    path("change_password/", views.change_password_view, name="change_password"),
    path("reset_password/", views.reset_password_view, name="reset_password"),
    path("reset_password_hash/<str:hash>", views.reset_password_hash, name="reset_password_hash"),
    path("paymentinfo/", views.paymentinfo_view, name="paymentinfo"),
    path("my_requests/", views.my_requests_view, name="my_requests"),
    path("my_ideas/", views.my_ideas_view, name="my_ideas"),
    path("all_requests/", views.all_requests_view, name="all_requests"),
    path("ideas_shared/", views.ideas_shared_view, name="ideas_shared"),
    path("request/<int:request_id>", views.request_view, name="request_view"),
    path("idea/<int:idea_id>", views.idea_view, name="idea_view"),
    path("stripe_create_account", views.stripe_create_account, name="stripe_create_account"),
    path("stripe_update_account", views.stripe_update_account, name="stripe_update_account"),
    path("stripe_create_intent/<int:idea_id>", views.stripe_create_intent, name="stripe_create_intent"),
    path("stripe_create_card/", views.stripe_create_card, name="stripe_create_card"),
    path("stripe/create_customer", views.stripe_create_customer, name="stripe_create_customer"),
    path("stripe/list_cards", views.stripe_list_cards, name="stripe_list_cards"),
    path("stripe/detach_card/<str:card_id>", views.stripe_detach_card, name="stripe_detach_card"),
    path("stripe_webhook", views.stripe_webhook, name="stripe_webhook"),
    path("api/get_my_requests_ids", api.get_my_requests_ids, name="get_my_requests_ids"),
    path("api/get_my_ideas_ids", api.get_my_ideas_ids, name="get_my_ideas_ids"),
    path("api/get_request/<int:id>", api.get_request, name="get_request"),
    path("api/get_idea/<int:id>", api.get_idea, name="get_idea"),
    path("api/new_request", api.new_request, name="new_request"),
    path("api/new_idea", api.new_idea, name="new_idea"),
    path("api/get_requests", api.get_requests, name="get_requests"),
    path("api/get_my_shared_ideas_ids", api.get_my_shared_ideas_ids, name="get_my_shared_ideas_ids"),
    path("api/get_ideas_from_requests_ids/<int:request_id>", api.get_ideas_from_requests_ids, name="get_ideas_from_requests_ids"),
    path("api/get_idea_preview/<int:id>", api.get_idea_preview, name="get_idea_preview"),
    path("api/accept_payment", api.accept_payment, name="accept_payment"),
    path("api/accept_banking", api.accept_banking, name="accept_banking"),
    path("showresponse", views.showresponse, name="showresponse"),
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)