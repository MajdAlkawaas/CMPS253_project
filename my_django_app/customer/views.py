from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Director, Customer, Queue, Category, User, Queueoperator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import director_required, queueoperator_required
from customer.forms import SingupForm, SigninForm, QueueOperatorSignup, EditForm, QueueOperatorForm
from customer.Myqueue import MyQueue
from guest.models import Guest
from guest.views import guest_view_uuid
from django.views.generic import CreateView
from django.core.mail import send_mail, BadHeaderError
from .forms import UserPasswordResetForm, UserSetPasswordForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.db.models import Q
from django.contrib import messages
import re
import datetime

def test_header(request):
    return render(request, 'Customer/test_header.html')

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

    return render(request, 'Customer/signup.html', {'form': form})

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
                if user.is_director == True:
                    return redirect('queueManagement-customer-page')
                elif user.is_queueoperator == True:
                    return redirect('QueueOperator')
            else:
                messages.error(request,'username or password not correct')
                print("HERE User is not logged in")
    else:
        form = SigninForm()
    context = {'form': form}
    return render(request, 'Customer/signin.html', context)

def welcome(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signin-customer-page')
    if not request.user.is_authenticated:
        return redirect('signin-customer-page')
    return render(request, 'Customer/welcome.html')

def forgot(request):
    return render(request, 'Customer/registration/forgot.html') 

def password_reset_done(request):
    return render(request, 'Customer/registration/password_reset_done.html') 

def password_reset_confirm(request):
    return render(request, 'Customer/registration/password_reset_confirm.html')

# @login_required()
# @director_required()
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
    return render(request, 'Customer/queueSetup.html') 

# @login_required()
# @director_required()

@login_required()
def edit(request,queue_id):

    queue            = Queue.objects.get(pk=queue_id)
    categories       = Category.objects.filter(Queue_id = queue_id)
    current_director = Director.objects.get(user_id = request.user)
    operators        = Queueoperator.objects.filter(Director=current_director)
    choices = []
    for element in operators:
        temp = (element, element.user.username)
        # print("element type: ", type(element))
        choices.append(temp)
    choices = tuple(choices)
    # print(choices)
    lista      = []
    for i in categories:
        lista.append(i.Name)

    categoriesStr = ",".join(lista)
    form          = EditForm(queue, categoriesStr, choices) 
    if request.method == "POST" and 'btnform1' in request.POST:
        form  = EditForm(queue, categoriesStr, choices, request.POST)
        if form.is_valid():
            queue      = Queue.objects.get(id=queue_id)
            queue.Name = form.cleaned_data.get("queueNameEdited")
            queue.save()

            listOfCategories = Category.objects.filter(Queue_id = queue_id)
            listNames = []
            for i in range(len(listOfCategories)):
                listNames.append(listOfCategories[i].Name)
            
            categories = form.cleaned_data.get("categoriesEdited")
            categories = categories.split(',')

            OperatorStringList = form.cleaned_data.get("queueOperator_list")
            # print(OperatorStringList)
            operatorsIDs = []
            for item in OperatorStringList:
                temp = re.findall("\d+", item)
                if(len(temp) > 0):
                    operatorsIDs.append(int(temp[0]))

            for i in operatorsIDs:
                op = Queueoperator.objects.get(user=i)
                op.Queue.add(queue)

            for category in categories:
                if category not in listNames:
                     Category.objects.create(Name = category,
                                             Queue = queue)

            for category in listOfCategories:
                if category.Name not in categories:
                    category.delete()
        return redirect('queueManagement-customer-page')

    elif request.method == 'POST' and 'btnform2' in request.POST:
        queue      = Queue.objects.get(id=queue_id)
        queue.delete() 

        return redirect('queueManagement-customer-page')

    context       = {'form': form, "queue" : queue, 'director':current_director}
    return render(request, 'Customer/edit.html', context) 


def home(request):
    return render(request, 'Customer/home.html')

def error(request):
    return render(request, 'Customer/error.html')

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
            return HttpResponseRedirect('/queueManagement/')
        else:
            print("Here input is invalid")
            print(form.cleaned_data)
            print(form.is_valid)
    else:
        print("HERE Request is not post")
        form = QueueOperatorSignup()

    return render(request, 'Customer/queueOperatorSignup.html', {'form': form})

chosenQueues = []
guestsOut = []
def QueueOperatorView(request):
    operator = Queueoperator.objects.get(user_id=request.user)
    opqueues = operator.Queue.all()
    form  = QueueOperatorForm(opqueues)
    context = {"form"          : form,
                "Queueoperator": operator}
    
    if request.method == 'POST' and 'logOut' in request.POST:
        logout(request)
        return redirect('signin-customer-page')
    if not request.user.is_authenticated:
        return redirect('signin-customer-page')
    if request.method == 'POST' and 'chooseQueue' in request.POST:
        print("----THIS IS THE CHOOSING QUEUE POST METHOD-----")
        # start = request.session.get('counter', 1)
        form  = QueueOperatorForm(opqueues, request.POST)
        # counter = start
        if form.is_valid():
            chosenQueue = form.cleaned_data.get("Queue_list")
            chosenQueues.append(chosenQueue)
            if not chosenQueue.Active:
                chosenQueue.Active = True
                chosenQueue.save()
            guests = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))
            guestNumbers = []
            for guest in guests:
                if guest not in guestsOut:
                    # guest.GuestNumber = counter
                    # counter+=1
                    guest.save()
                    guestsOut.append(guest)
                guestNumbers.append(guest.GuestNumber)
            # request.session['counter'] = counter + 1
            if len(guestNumbers)!=0:
                print(guestNumbers)
                context["opqueues"] = opqueues
                context["guests"] = guests
                context["guestNumbers"] = min(guestNumbers)
                return render(request, 'Customer/queueOperator.html', context)
            else:
                return render(request, 'Customer/queueOperator.html', context)

    elif request.method == 'POST' and 'btnserve' in request.POST:
        print("----THIS IS THE SERVING POST METHOD-----")
        form  = QueueOperatorForm(opqueues, request.POST)
        # start = request.session.get('counter', 1)
        # counter = start
        if form.is_valid():
            chosenQueue = chosenQueues[0]
            guests = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))
            guestNumbers = []
            for guest in guests:
                guestNumbers.append(guest.GuestNumber)
            if len(guestNumbers)!=0:
                guestNumbersFinal = []
                theOne = min(guestNumbers)
                guestToBeDeleted = Guest.objects.get(Q(GuestNumber = theOne) & Q(Queue = chosenQueue))
                guestToBeDeleted.Served = True
                guestToBeDeleted.endOfServiceTime = datetime.datetime.now()
                guestToBeDeleted.save()
                guestsFinal = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))
                
                for guest in guestsFinal:
                    guestNumbersFinal.append(guest.GuestNumber)
                if len(guestNumbersFinal)!=0:
                    context["opqueues"] = opqueues
                    context["guests"] = guestsFinal
                else:
                    context["opqueues"] = opqueues
                    context["guests"] = guestsFinal
                    context["guestNumbers"] = min(guestNumbersFinal)
                # context["counter"] = counter
                return render(request, 'Customer/queueOperator.html', context)
            else:
                context["opqueues"] = opqueues
                context["guests"] = guests
                return render(request, 'Customer/queueOperator.html', context)
    
    
    elif request.method == 'POST' and 'btnRequest' in request.POST:
        print("----THIS IS THE REQUEST QUEUE POST METHOD-----")
        currentGuestPhoneNumber = ""
        form  = QueueOperatorForm(opqueues, request.POST)
        # start = request.session.get('counter', 1)
        # counter = start
        if form.is_valid():
            chosenQueue = chosenQueues[0]
            guests = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))
            guestNumbers = []
            for guest in guests:
                guestNumbers.append(guest.GuestNumber)
            # if len(guestNumbers)!=0:
            theOne = min(guestNumbers)
            guestToBeDeleted = Guest.objects.get(Q(GuestNumber = theOne) & Q(Queue = chosenQueue))
            guestToBeDeleted.beginOfServiceTime = datetime.datetime.now()
            guestToBeDeleted.save()
            currentGuestPhoneNumber = guestToBeDeleted.PhoneNumber
            print(datetime.datetime.now())
            send_sms(guestToBeDeleted.Name, currentGuestPhoneNumber)
            context["opqueues"] = opqueues
            context["guests"] = guests
            context["guestNumbers"] = min(guestNumbers)
            return render(request, 'Customer/queueOperator.html', context)

    elif request.method == 'POST' and 'btnremove' in request.POST:
        print("----THIS IS THE REMOVE QUEUE POST METHOD-----")
        form  = QueueOperatorForm(opqueues, request.POST)
        # start = request.session.get('counter', 1)
        # counter = start
        if form.is_valid():
            chosenQueue = chosenQueues[0]
            guests = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))
            guestNumbers = []
            for guest in guests:
                guestNumbers.append(guest.GuestNumber)
            if len(guestNumbers)!=0:
                guestNumbersFinal = []
                theOne = min(guestNumbers)
                guestToBeDeleted = Guest.objects.get(Q(GuestNumber = theOne) & Q(Queue = chosenQueue))
                guestToBeDeleted.Kickedout = True
                guestToBeDeleted.save()
                guestsFinal = Guest.objects.filter(Q(WalkedAway=False) & Q(Kickedout=False) & Q(Served=False) & Q(Queue = chosenQueue))

                for guest in guestsFinal:
                    guestNumbersFinal.append(guest.GuestNumber)
                if len(guestNumbersFinal)!=0:
                    context["opqueues"] = opqueues
                    context["guests"] = guestsFinal
                else:
                    context["opqueues"] = opqueues
                    context["guests"] = guestsFinal
                    context["guestNumbers"] = min(guestNumbersFinal)
                # context["counter"] = counter
                return render(request, 'Customer/queueOperator.html', context)
            else:
                context["opqueues"] = opqueues
                context["guests"] = guests
                return render(request, 'Customer/queueOperator.html', context)

    return render(request, 'Customer/queueOperator.html', context)


def password_reset_request(request):
    print("HERE: 01")
    if request.method == "POST":
        print("HERE: 02")
        password_reset_form = UserPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            print("HERE: 03")
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                print("HERE: 04")
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "Customer/registration/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect ("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="Customer/registration/password_reset.html", 
                    context={"password_reset_form":password_reset_form})

def queueManagement(request):
    current_director = Director.objects.get(user_id = request.user)
    data             = Queue.objects.filter(Director = current_director)
    operators        = Queueoperator.objects.filter(Director=current_director)
    context  = {"data"    : data, 
               "director" : current_director,
               "operators": operators}
    
    if request.method == 'POST':
        logout(request)
        return redirect('signin-customer-page')
    if not request.user.is_authenticated:
        return redirect('signin-customer-page')
               
    return render(request, 'Customer/queueManagement.html', context) 

from reportlab.pdfgen import canvas  
from django.http import HttpResponse  
from reportlab.lib.utils import ImageReader
import os
def getpdf(request):   
    print("HERE:", os.getcwd())
    current_director = Director.objects.get(user_id = request.user)
    current_customer = current_director.Customer
    print("customer:", current_customer)
    QRcode_path = os.path.join(os.getcwd(), str(current_director.QRcode))
    # QRcode_path = "file:///C:/Users/student/Desktop/Project/CMPS253_project/my_django_app/QRcodes/qr_code-0aa6dfc8-e92a-4f01-8d80-70e99fb0f48f.png"
    QRcode = ImageReader(QRcode_path)
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename="QRcode.pdf" '  
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 55)  
    p.drawImage(QRcode, 10, 10, mask='auto')
    p.drawString(100,700, str(current_customer))  

    p.showPage()  
    p.save()  
    return response

from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse
from twilio.rest import Client


def send_sms(guestName, guestPhoneNumber):
    message_to_broadcast = ("Mr/Ms {} You may be served now".format(guestName))
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    print("HERE", settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    print(client)
    print(guestPhoneNumber)
    if guestPhoneNumber:
        client.messages.create(to=guestPhoneNumber,
                                from_=settings.TWILIO_NUMBER,
                                body=message_to_broadcast)
        print("HERE: it is done")


