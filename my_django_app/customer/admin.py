from django.contrib import admin

# Register your models here.
from .models import Customer, Director
admin.site.register(Customer)
admin.site.register(Director)