from django.urls import path
from . import views


urlpatterns = [
    path('signin/', views.signin, name="signin-customer-page"),
    path('signup/', views.signup, name="signup-customer-page"),
    path('forgot/', views.forgot, name="forgot-customer-page"),
    path('queueSetup/', views.queueSetup, name="queueSetup-customer-page"),
    path('queueManagement/', views.queueManagement, name="queueManagement-customer-page"),
    path('edit/', views.edit, name="edit-customer-page"),
    path('', views.home, name="customer-home"),
]
