from django.shortcuts import render
from .models import Director, Customer

def signup(request):
    if request.method == "POST":
        print(request.POST)
        value = request.POST
        print(value)
        Director.objects.create(FirstName=value.get('fname'),
                                LastName=value.get('lname'),
                                username=value.get('username'),
                                EmailAddress=value.get('email'),
                                password=value.get('password'))
        Customer.objects.create(Name=value.get('Name'),
                                ContactFirstName=value.get('ContactFirstName'),
                                ContactLastName=value.get('ContactLastName'),
                                EmailAddress=value.get('EmailAddress'),
                                PhoneNumber=value.get('PhoneNumber')
                                )
                                
    context ={}
    return render(request, 'customer/signup.html', context)

def signin(request):
    return render(request, 'customer/signin.html')

def forgot(request):
    return render(request, 'customer/forgot.html') 

def queueSetup(request):
    return render(request, 'customer/queueSetup.html') 

def queueManagement(request):
    return render(request, 'customer/queueManagement.html') 

def edit(request):
    return render(request, 'customer/edit.html') 
