from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from customer.models import Customer,Director, Category, Queue, User
from guest.models import Guest
from guest.forms import GuestForm
from django.http import HttpResponse, Http404
from django.db import models
import qrcode
import urllib.parse
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


def guest_view_uuid(request, director_uuid):
    director_uuid_hex = director_uuid.hex
    try:
        current_director = Director.objects.get(director_uuid= director_uuid_hex)
    except Director.DoesNotExist:
        raise Http404("cusotmer with uuid {} doesn't exit".format(director_uuid_hex)) 

    user     = User.objects.get(pk=current_director.user_id)
    customer = Customer.objects.get(pk=current_director.Customer.id)
    queues   = Queue.objects.filter(Director = current_director.user_id)
    categories = []        
    categories = Category.objects.none()
    for queue in queues:    
        categories = categories | Category.objects.filter(Queue = queue)


    form = GuestForm(categories = categories)
    context = {
        'queues'    : queues,
        'director'  : user,
        'customer'  : customer,
        'categories': categories,
        'form'      : form
    }

    if request.method == 'POST':

        start = request.session.get('counter', 1)
        counter = start
        form = GuestForm(categories, request.POST)
        if form.is_valid():

            myQueue       = form.cleaned_data.get("categories_list").Queue
            if(len(Guest.objects.filter(Queue = myQueue))==0):
                myGuestsNumber = 1
            else:
                lastGuest = Guest.objects.filter(Queue = myQueue).last()
                myGuestsNumber= lastGuest.GuestNumber + 1


            guest01 = Guest.objects.create(Name        = form.cleaned_data.get("name"),
                                           PhoneNumber = form.cleaned_data.get("phoneNumber"),
                                           Category    = form.cleaned_data.get("categories_list"),
                                           Director    = current_director,
                                           GuestNumber = myGuestsNumber,
                                           Customer    = customer,
                                           Queue       = form.cleaned_data.get("categories_list").Queue)
            request.session['counter'] = counter + 1
            context['guest01'] = guest01
            return HttpResponseRedirect('../../guestWaitingPage/' + str(guest01.id))
        else: 
            print("------------------------")
            print("guest.views\n HERE WRONG")
            print("------------------------")

    return render(request, 'guest/guest.html', context) 


def guest_waiting_page(request, guest_id):
    guest = Guest.objects.get(id=guest_id)
    if request.method == 'POST':
        guest.WalkedAway = True
        guest.save()
    context = {"guest":guest}
    return render(request, "guest/waitingPage.html", context)
