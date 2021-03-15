from django.urls import path
from . import views

urlpatterns = [
    path('guest/', views.guest, name="guest-page"),
]