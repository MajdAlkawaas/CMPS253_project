from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Director, Customer, Queue
from django.contrib.auth import authenticate, login, logout
import json
from customer.forms import SingupForm


def signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SingupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            Director.objects.create(**form.cleaned_data)
            # redirect to a new URL:
            return HttpResponseRedirect('/signin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SingupForm()

    return render(request, 'customer/signup.html', {'form': form})


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
