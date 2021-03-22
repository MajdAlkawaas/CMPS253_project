from django.shortcuts import render, redirect
from customer.models import Customer,Director, Category, Queue
from guest.models import Guest
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
        guest01 = Guest(PhoneNumber       = value.get('PhoneNumber')
        )
        guest01.save()
        return redirect("guest-waiting-page")
    return render(request, 'guest/guest.html') 

def guest_view_id(request, queue_id):
    if request.method == "POST":
        return redirect("guest-waiting-page")
        # return render(request, 'guest/guest_beta.html') 
    else:
        try:
            # queue = Customer.objects.get(queue_uuid= queue_uuid)
            queue = Queue.objects.get(pk= queue_id)
        except Queue.DoesNotExist:
            raise Http404("Queue with uuid {} doesn't exit".format(queue_id)) 
        director   = Director.objects.get(pk= queue.Director.id)
        customer   = Customer.objects.get(pk=director.Customer.id)
        categories = Category.objects.all().filter(Queue_id=queue_id)

        print(categories)
        for category in categories:
            print(category.Name)

        context = {
            'queue'     : queue,
            'director'  : director,
            'customer'  : customer,
            'categories': categories
        }
        # context = {}

        return render(request, 'guest/guest_beta.html', context) 








def guest_view_uuid(request, queue_uuid):
    queue_uuid_hex = queue_uuid.hex
    try:
        queue = Queue.objects.get(queue_uuid= queue_uuid_hex)
    except Queue.DoesNotExist:
        raise Http404("cusotmer with uuid {} doesn't exit".format(queue_uuid_hex)) 

    director   = Director.objects.get(pk= queue.Director.id)
    customer   = Customer.objects.get(pk=director.Customer.id)
    categories = Category.objects.all().filter(Queue_id=queue.id)


    print(categories)
    for category in categories:
        print(category.Name)

    context = {
        'queue'     : queue,
        'director'  : director,
        'customer'  : customer,
        'categories': categories
    }

    return render(request, 'guest/guest_beta.html', context) 

# def guest(request):

#     return render(request, 'guest/guest.html') 


def save(domain="http://127.0.0.1:8000/", *args, **kwargs):
        # Retrive all the queues
        # queues = Queue.objects.all()

        # Retrive all the queues that don't have QR codes
        queues = Queue.objects.filter(QRcode='')
        for queue in queues:
            print("Queue ID: {} \n Queue Name: {}".format(queue.id, queue.Name))

            queue_url = urllib.parse.urljoin(domain, 'queue/uuid/{}'.format(str(queue.queue_uuid)))
            qrcode_img = qrcode.make(queue_url)
        
            canvas = Image.new('RGB', (450,450), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'(qr_code-{queue.queue_uuid}.png'
            buffer = BytesIO()
            canvas.save(buffer,'PNG')
            queue.QRcode.save(fname, File(buffer), save=False)
            canvas.close()
            models.Model.save(queue, *args,**kwargs)

def guest_waiting_page(request):
    return render(request, "guest/waitingPage.html")
