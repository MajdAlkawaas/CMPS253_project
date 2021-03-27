from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from customer.models import Director, Customer, Queue, User
from django.contrib.auth import authenticate, login, logout
import json
from customer.forms import SingupForm, signinForm, Test_signin, Test_signup
from django.views.generic import CreateView


def signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SingupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username     = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user         = authenticate(username=username, password=raw_password)
            login(request, user)

            director01 = Director(FirstName = form.cleaned_data.get('fname'),
                                  LastName  = form.cleaned_data.get('lname'),
                                  Customer  = form.cleaned_data.get('Customer'))

            return HttpResponseRedirect('/signin/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SingupForm()

    return render(request, 'customer/signup.html', {'form': form})

def test_signup(request):
    if request.method == 'POST':
        print("HERE00**")
        form = Test_signup(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            print("HERE00")
            print("---------------------")
            print(request)
            print("---------------------")
            return HttpResponseRedirect('/test/signin/')
        else:
            print(form.cleaned_data)
            print(form.is_valid)
    # if a GET (or any other method) we'll create a blank form
    else:
        print("HERE01")
        print("---------------------")
        print(request)
        print("---------------------")

        form = Test_signup()

    return render(request, 'customer/signup.html', {'form': form})


def test_signin(request):
    print("Sign in 01")
    if request.method == 'POST':
        print("Sign in 02")
        form = Test_signin(request.POST)
        if form.is_valid():
            print("Sign in 03")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("NOT FUCK YOU")
                return redirect('test-welcome-customer-page')
            else:
                print("FUCK YOU")
    else:
        form = Test_signin()
    context = {'form': form}
    return render(request, 'customer/test_signin.html', context)

def test_welcome(request):
    return render(request, 'customer/welcome.html')

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
