from django.shortcuts import render
from customer.models import Customer,Director, Category, Queue
from django.http import HttpResponse, Http404


def guest_view_id(request, queue_id):
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
