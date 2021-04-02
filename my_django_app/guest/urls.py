from django.urls import path
from . import views

urlpatterns = [   
    # Request a queue guest page using queue_uuid
    path('customer/uuid/<uuid:director_uuid>', views.guest_view_uuid, name="queue-page"),

    # Request a queue guest page using queue_id
    path('queue/id/<int:queue_id>', views.guest_view_id, name="queue-page"),


    path('guest/', views.guest, name="guest-page"),

    path('guestWaitingPage', views.guest_waiting_page, name="guest-waiting-page"),

]