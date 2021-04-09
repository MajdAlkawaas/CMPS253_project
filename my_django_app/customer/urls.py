from django.urls import path
from . import views


urlpatterns = [
    path('error/', views.error, name="error"),
    path('welcome/', views.welcome, name="welcome-customer-page"),
    path('signin/', views.signin, name="signin-customer-page"),
    path('signup/', views.signup, name="signup-customer-page"),
    path('forgot/', views.forgot, name="forgot-customer-page"),
    path('queueSetup/', views.queueSetup, name="queueSetup-customer-page"),
    path('queueManagement/', views.queueManagement, name="queueManagement-customer-page"),
    path('edit/<int:queue_id>', views.edit, name="edit-customer-page"),
    path('', views.home, name="customer-home"),
    path("QueueOperatorSignup/", views.QueueOperatorSignupView, name="QueueOperatorSignup"),
    path("QueueOperator/", views.QueueOperator, name="QueueOperator"),
]
