from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Director, Customer, Queue, Category, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import director_required, queueoperator_required
from customer.forms import SingupForm, SigninForm, QueueOperatorSignup
from django.views.generic import CreateView

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
        category = value.get("categories")
        category = category.split(',')

        director = Director(
            user = request.user,
        )


        queue = Queue(
            Name = value.get('queueName'),
            Active = False,
            Director = director,
        )
        queue.save()

        for i in range(len(category)):
            cat = Category(
                Name = category[i],
                Queue = queue
            )
            cat.save()
        return redirect('queueManagement-customer-page')
    return render(request, 'customer/queueSetup.html') 

@login_required()
@director_required()
def queueManagement(request):
    data = Queue.objects.all()
    director = Director(user = request.user)
    context = {"data" : data, "director" : director}
    return render(request, 'customer/queueManagement.html', context) 


@login_required()
def edit(request,queue_id):
    if request.method == "POST":
        value = request.POST

        queue      = Queue.objects.get(id=queue_id)
        queue.Name = value.get('queueNameEdited')
        queue.save()

        listOfCategories = Category.objects.all().filter(Queue_id = queue_id)
        for i in listOfCategories:
            listOfCategories.delete()

        categories = value.get("categoriesEdited")
        categories = categories.split(',')

        for i in range(len(categories)):
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