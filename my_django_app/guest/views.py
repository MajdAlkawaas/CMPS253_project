from django.shortcuts import render, redirect
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


def guest(request):
    if request.method == "POST":
        value = request.POST
        guest01 = Guest(PhoneNumber = value.get('PhoneNumber'))
        guest01.save()
        return redirect("guest-waiting-page")
    return render(request, 'guest/guest.html') 


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

    print("------------------------")
    print("guest.views \nHERE Categories type:\n", type(categories))
    print("------------------------")

    form = GuestForm(categories = categories)
    # form = GuestForm()
    if request.method == 'POST':
        form = GuestForm(categories, request.POST)
        if form.is_valid():
            
            print("guest.views\n HERE: ------CLEANED DATA------ \n", form.cleaned_data)
            print("------------------------")
            guest01 = Guest.objects.create(Name        = form.cleaned_data.get("name"),
                                           PhoneNumber = form.cleaned_data.get("phoneNumber"),
                                           Category    = form.cleaned_data.get("categories_list"),
                                           Director    = current_director,
                                           Customer    = customer,
                                           Queue       = form.cleaned_data.get("categories_list").Queue)
            print("GUEST obj\n", guest01) 
            return redirect('guest-waiting-page')
        else: 
            print("------------------------")
            print("guest.views\n HERE WRONG")
            print("------------------------")

    context = {
        'queues'    : queues,
        'director'  : user,
        'customer'  : customer,
        'categories': categories,
        'form'      : form
    }
    return render(request, 'guest/guest.html', context) 


def guest_waiting_page(request):
    return render(request, "guest/waitingPage.html")
