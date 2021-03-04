from django.db import models
import datetime
# Create your models here.




class Customer(models.Model):
    Name             = models.CharField(max_length=120)
    ContactFirstName = models.CharField(max_length=50)
    ContactLastName  = models.CharField(max_length=50)
    EmailAddress     = models.EmailField(max_length=250)
    PhoneNumber      = models.CharField(max_length=50)
    CreatedAt        = models.DateTimeField(auto_now=True)

class Director(models.Model):
    FirstName    = models.CharField(max_length=50)
    LastName     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50)
    EmailAddress = models.EmailField(max_length=250)
    password     = models.CharField(max_length=50)
    CreatedAt    = models.DateTimeField(auto_now=True)
    Customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Queue(models.Model):
    Name      = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now=True)
    Active    = models.BooleanField()
    Director  = models.ForeignKey(Director, on_delete=models.CASCADE)

class Queueoperator(models.Model):
    FirstName    = models.CharField(max_length=50)
    LastName     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50)
    EmailAddress = models.EmailField(max_length=250)
    password     = models.CharField(max_length=50)
    CreatedAt    = models.DateTimeField(auto_now=True)
    Customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Director     = models.ForeignKey(Director, on_delete=models.CASCADE)
    Queue        = models.ForeignKey(Queue, on_delete=models.CASCADE)

class Category(models.Model):
    Name      = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now=True)
    Queue     = models.ForeignKey(Queue, on_delete=models.CASCADE)



 
 

