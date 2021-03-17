from django.urls import path
from . import views

urlpatterns = [   
    # Request a queue guest page using queue_uuid
    path('queue/uuid/<uuid:queue_uuid>', views.guest_view_uuid, name="queue-page"),

    # Request a queue guest page using queue_id
    path('queue/id/<int:queue_id>', views.guest_view_id, name="queue-page"),

    path('guestWaitingPage', views.guest_waiting_page, name="guest-waiting-page"),


]