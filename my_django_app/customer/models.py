from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
import uuid
import qrcode
import urllib.parse
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# Create your models here.




class Customer(models.Model):
    Name             = models.CharField(max_length=120)
    ContactFirstName = models.CharField(max_length=50)
    ContactLastName  = models.CharField(max_length=50)
    EmailAddress     = models.EmailField(max_length=250)
    PhoneNumber      = models.CharField(max_length=50)
    CreatedAt        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Name
    

class User(AbstractUser):
    is_director      = models.BooleanField(default=False)
    is_queueoperator = models.BooleanField(default=False)


class Director(models.Model):
    user          = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    CreatedAt     = models.DateTimeField(auto_now=True)
    Customer      = models.ForeignKey(Customer, on_delete=models.CASCADE)
    director_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    QRcode        = models.ImageField(upload_to="QRcodes/", null=True, blank=True)
   
    def save(self, domain="http://127.0.0.1:8000/", *args, **kwargs):
        director_uuid = urllib.parse.urljoin(domain, 'customer/uuid/{}'.format(str(self.director_uuid)))
        qrcode_img = qrcode.make(director_uuid)
        
        canvas = Image.new('RGB', (450,450), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'(qr_code-{self.director_uuid}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.QRcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)

class Queue(models.Model):
    Name       = models.CharField(max_length=50)
    CreatedAt  = models.DateTimeField(auto_now=True)
    Active     = models.BooleanField()
    Director   = models.ForeignKey(Director, on_delete=models.CASCADE)
    
    
                
class Queueoperator(models.Model):
    user      = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    CreatedAt = models.DateTimeField(auto_now=True)
    Customer  = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Director  = models.ForeignKey(Director, on_delete=models.CASCADE)
    Queue     = models.ManyToManyField(Queue)

class Category(models.Model):
    Name      = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now=True)
    Queue     = models.ForeignKey(Queue, on_delete=models.CASCADE)



 
 

