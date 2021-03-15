from django.shortcuts import render

def guest(request):
    return render(request, 'guest/guest.html') 
