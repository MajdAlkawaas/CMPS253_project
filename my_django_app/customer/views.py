from django.shortcuts import render, redirect
from .models import Director, Customer, Queue
from django.contrib.auth import authenticate, login, logout
import json

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
        return redirect("signin-customer-page")
    return render(request, 'customer/signup.html')

def signin(request):
    if request.method == "POST":
        value = request.POST
        username = value.get('username')
        password = value.get('password')
        # username = request.POST.get('username')
        # password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(user)
            
        if user is not None:
            login(request, user)
            return redirect("queueSetup-customer-page")
        else:
            return render(request, "customer/signin.html")
    return render(request, 'customer/signin.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

def queueSetup(request):
    if request.method == "POST":
        value = request.POST
        user = request.Director
        queue01 = Queue(Name=value.get("queueName"), Director=user, Active=False)
        queue01.save()


        tags = json.loads(request.POST.get("categories"))
        print(tags)

    return render(request, 'customer/queueSetup.html') 

def queueManagement(request):
    return render(request, 'customer/queueManagement.html') 

def edit(request):
    return render(request, 'customer/edit.html') 

def home(request):
    return render(request, 'customer/home.html')
