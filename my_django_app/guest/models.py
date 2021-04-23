from django.db import models
import datetime


class Guest(models.Model):
    Name               = models.CharField(max_length=50)
    PhoneNumber        = models.CharField(max_length=50)
    WalkedAway         = models.BooleanField(default=False)
    Kickedout          = models.BooleanField(default=False)
    Served             = models.BooleanField(default=False)
    CreatedAt          = models.DateTimeField(auto_now=True)
    GuestNumber        = models.PositiveSmallIntegerField(null=True, blank=True)
    beginOfServiceTime = models.DateTimeField(null=True, blank=True)
    endOfServiceTime   = models.DateTimeField(null=True, blank=True)
    Customer           = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    Director           = models.ForeignKey('customer.Director', on_delete=models.CASCADE)
    Queue              = models.ForeignKey('customer.Queue', on_delete=models.CASCADE)
    Category           = models.ForeignKey('customer.Category', on_delete=models.CASCADE)
    Queueoperator      = models.ForeignKey('customer.Queueoperator', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.Name
