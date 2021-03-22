from django.db import models
import datetime


class Guest(models.Model):
    PhoneNumber = models.CharField(max_length=50)
    WalkedAway = models.BooleanField(null=True)
    Kickedout  = models.BooleanField()
    Served     = models.BooleanField()
    CreatedAt  = models.DateTimeField(auto_now=True)
    GuestNumber = models.PositiveSmallIntegerField()
    beginOfServiceTime = models.DateTimeField(blank=True)
    endOfServiceTime = models.DateTimeField(blank=True)
    Customer   = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    Director   = models.ForeignKey('customer.Director', on_delete=models.CASCADE)
    Queue      = models.ForeignKey('customer.Queue', on_delete=models.CASCADE)
    Category = models.ForeignKey('customer.Category', on_delete=models.CASCADE)
    Queueoperator = models.ForeignKey('customer.Queueoperator', on_delete=models.CASCADE)

