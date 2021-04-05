from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Director, Customer, Queue, Category, User, Queueoperator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import director_required, queueoperator_required
from customer.forms import SingupForm, SigninForm, QueueOperatorSignup
from django.views.generic import CreateView
import json

def signup(request):
    if request.method == 'POST':
        print("HERE Request is post")
        form = SingupForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            print("HERE Input is valid")
            print("---------------------")
            print(request)
            print("---------------------")
            return HttpResponseRedirect('/signin/')
        else:
            print("Here input is invalid")
            print(form.cleaned_data)
            print(form.is_valid)
    # if a GET (or any other method) we'll create a blank form
    else:
        print("HERE Request is not post")
        form = SingupForm()

    return render(request, 'customer/signup.html', {'form': form})

def signin(request):
    print("Sign in 01")
    if request.method == 'POST':
        print("Sign in 02")
        form = SigninForm(request.POST)
        if form.is_valid():
            print("Sign in 03")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("HERE User {} is logged in".format(username))
                return redirect('welcome-customer-page')
            else:
                print("HERE User is not logged in")
    else:
        form = SigninForm()
    context = {'form': form}
    return render(request, 'customer/signin.html', context)

def welcome(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signin-customer-page')
    if not request.user.is_authenticated:
        return redirect('signin-customer-page')
    return render(request, 'customer/welcome.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

@login_required()
@director_required()
def queueSetup(request):
    if request.method == "POST":
        value = request.POST
        
        director = Director.objects.get(user = request.user)
        queue = Queue.objects.create(Name = value.get('queueName'),
                                     Active = False,
                                     Director = director)

        category = value.get("categories")
        category = category.split(',')
        for i in range(len(category)):
            category[i] = category[i].rstrip().lstrip()
            Category.objects.create(Name = category[i], Queue = queue)

        return redirect('queueManagement-customer-page')
    return render(request, 'customer/queueSetup.html') 

@login_required()
@director_required()
def queueManagement(request):
    current_director = Director.objects.get(user_id = request.user)
    data             = Queue.objects.filter(Director = current_director)
    operators        = Queueoperator.objects.filter(Director=current_director)
    context  = {"data"    : data, 
               "director" : current_director,
               "operators": operators}
               
    return render(request, 'customer/queueManagement.html', context) 


@login_required()
def edit(request,queue_id):
    if request.method == "POST":
        value = request.POST

        queue      = Queue.objects.get(id=queue_id)
        queue.Name = value.get('queueNameEdited')
        queue.save()

        listOfCategories = Category.objects.filter(Queue_id = queue_id)
        for i in listOfCategories:
            listOfCategories.delete()

        categories = value.get("categoriesEdited")
        categories = categories.split(',')

        for i in range(len(categories)):
            #Q: What is happening here??
            category = Category(
                Name  = categories[i],
                Queue = queue
            )
            category.save()

        return redirect('queueManagement-customer-page')

    queue      = Queue.objects.get(pk=queue_id)
    categories = Category.objects.all().filter(Queue_id = queue_id)
    lista      = []

    for i in categories:
        lista.append(i.Name)

    categoriesStr = ",".join(lista)
    context       = {"queue" : queue, "categoriesStr" : categoriesStr}

    return render(request, 'customer/edit.html', context) 

@login_required()
@director_required()
def home(request):
    return render(request, 'customer/home.html')

def error(request):
    return render(request, 'customer/error.html')


@login_required()
@director_required()
# @queueoperator_required()
def QueueOperatorSignupView(request):
    if request.method == 'POST':
        print("HERE Request is post")
        form = QueueOperatorSignup(request.POST, user=request.user)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            print("HERE Input is valid")
            print("---------------------")
            print(request)
            print("---------------------")
            return HttpResponseRedirect('/signin/')
        else:
            print("Here input is invalid")
            print(form.cleaned_data)
            print(form.is_valid)
    # if a GET (or any other method) we'll create a blank form
    else:
        print("HERE Request is not post")
        form = QueueOperatorSignup()

    return render(request, 'customer/QueueOperatorSignup.html', {'form': form})