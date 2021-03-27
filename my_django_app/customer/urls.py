from django.urls import path
from . import views

urlpatterns = [

    path('test/signin/', views.test_signin, name="test-signin-customer-page"),
    path('test/signup/', views.test_signup, name="test-signup-customer-page"),
     path('test/welcome/', views.test_welcome, name="test-welcome-customer-page"),

    path('signin/', views.signin, name="signin-customer-page"),
    
    path('signup/', views.signup, name="signup-customer-page"),
    path('forgot/', views.forgot, name="forgot-customer-page"),
    path('queueSetup/', views.queueSetup, name="queueSetup-customer-page"),
    path('queueManagement/', views.queueManagement, name="queueManagement-customer-page"),
    path('edit/', views.edit, name="edit-customer-page"),
    path('', views.home, name="customer-home"),
]
