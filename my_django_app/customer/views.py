from django.shortcuts import render, redirect
from .models import Director, Customer
from django.contrib.auth.models import User, auth

def signup(request):
    if request.method == "POST":
        value = request.POST

        customer01 = Customer(Name=value.get('Name'),
                             ContactFirstName=value.get('ContactFirstName'),
                             ContactLastName=value.get('ContactLastName'),
                             EmailAddress=value.get('EmailAddress'),
                             PhoneNumber=value.get('PhoneNumber'))
        customer01.save()
        director01 = Director(FirstName=value.get('fname'),
                                LastName=value.get('lname'),
                                username=value.get('username'),
                                EmailAddress=value.get('email'),
                                password=value.get('password'),
                                Customer = customer01)
        director01.save()
        return redirect("singin-customer-page")
                                
    return render(request, 'customer/signup.html')

def signin(request):
    print(request)
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
            
        if user is not None:
            auth.login(request, user)
            return redirect("queueSetup-customer-page")
        else:
            return redirect("singin-customer-page")
    print(request.POST)
    return render(request, 'customer/signin.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

def queueSetup(request):
    return render(request, 'customer/queueSetup.html') 

def queueManagement(request):
    return render(request, 'customer/queueManagement.html') 

def edit(request):
    return render(request, 'customer/edit.html') 
