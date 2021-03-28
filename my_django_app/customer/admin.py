from django.contrib import admin

# Register your models here.
from .models import User, Customer, Director, Queue, Category
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Director)
admin.site.register(Queue)
admin.site.register(Category)