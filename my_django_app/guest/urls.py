from django.urls import path
from . import views

urlpatterns = [   
    # Request a queue guest page using queue_uuid
    path('customer/uuid/<uuid:director_uuid>', views.guest_view_uuid, name="guest-page"),
    path('guestWaitingPage', views.guest_waiting_page, name="guest-waiting-page"),

]