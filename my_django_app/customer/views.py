from django.shortcuts import render

def signup(request):
    return render(request, 'customer/signup.html')

def signin(request):
    return render(request, 'customer/signin.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

def queueSetup(request):
    return render(request, 'customer/queueSetup.html') 
