from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Director, Customer, Queue, Category
from django.contrib.auth import authenticate, login, logout
import json
from customer.forms import SingupForm, signinForm


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
        form = signinForm(request.POST)

        return redirect("queueSetup-customer-page")
    
    return render(request, 'customer/signin.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

def queueSetup(request):
    if request.method == "POST":
        value = request.POST
        category = value.get("categories")
        category = category.split(',')

        queue = Queue(
            Name = value.get('queueName'),
            Active = False,
        )
        queue.save()

        for i in range(len(category)):
            cat = Category(
                Name = category[i],
                Queue = queue
            )
            cat.save()

    return render(request, 'customer/queueSetup.html') 

def queueManagement(request):
    return render(request, 'customer/queueManagement.html') 

def edit(request):
    return render(request, 'customer/edit.html') 

def home(request):
    return render(request, 'customer/home.html')
