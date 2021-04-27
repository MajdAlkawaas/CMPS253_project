from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import UserPasswordResetForm, UserSetPasswordForm


urlpatterns = [
    # path('pdf/test/', views.getpdf_test, name="pdf-file"),

    path('pdf/', views.getpdf, name="pdf-file"),

    path('password_reset/', 
        auth_views.PasswordResetView.as_view(
            template_name='Customer/registration/forgot.html',
            form_class=UserPasswordResetForm),
        name='password_reset'
        ),
    
    path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(
            template_name="Customer/registration/password_reset_confirm.html",
            form_class=UserSetPasswordForm), 
        name='password_reset_confirm'
        ),



    path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(
            template_name='Customer/registration/password_reset_done.html'), 
        name='password_reset_done'
        ),
    
    
    path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(
            template_name='Customer/registration/password_reset_complete.html'), 
        name='password_reset_complete'
        ),  

    
    
    path('error/', views.error, name="error"),
    path('welcome/', views.welcome, name="welcome-customer-page"),
    path('signin/', views.signin, name="signin-customer-page"),
    path('signup/', views.signup, name="signup-customer-page"),
    # path('forgot/', views.forgot, name="forgot-customer-page"),
    path('queueSetup/', views.queueSetup, name="queueSetup-customer-page"),
    path('queueManagement/', views.queueManagement, name="queueManagement-customer-page"),
    path('edit/<int:queue_id>', views.edit, name="edit-customer-page"),
    path('', views.home, name="customer-home"),
    path("QueueOperatorSignup/", views.QueueOperatorSignupView, name="QueueOperatorSignup"),
    path("QueueOperator/", views.QueueOperatorView, name="QueueOperator"),
]
