from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin, name="singin-customer-page"),
    path('signup/', views.signup, name="singup-customer-page"),
    path('forgot/', views.forgot, name="forgot-customer-page"),
    path('queueSetup/', views.queueSetup, name="queueSetup-customer-page"),
]
