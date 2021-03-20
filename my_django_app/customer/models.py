from django.db import models
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

class Director(models.Model):
    FirstName    = models.CharField(max_length=50)
    LastName     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50)
    EmailAddress = models.EmailField(max_length=250)
    password     = models.CharField(max_length=50)
    CreatedAt    = models.DateTimeField(auto_now=True)
    Customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Queue(models.Model):
    Name       = models.CharField(max_length=50)
    CreatedAt  = models.DateTimeField(auto_now=True)
    Active     = models.BooleanField()
    Director   = models.ForeignKey(Director, on_delete=models.CASCADE)
    queue_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    QRcode     = models.ImageField(upload_to="QRcodes/", null=True, blank=True)
   
    def save(self, domain="http://127.0.0.1:8000/", *args, **kwargs):
        queue_url = urllib.parse.urljoin(domain, 'queue/uuid/{}'.format(str(self.queue_uuid)))
        qrcode_img = qrcode.make(queue_url)
        
        canvas = Image.new('RGB', (450,450), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'(qr_code-{self.queue_uuid}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.QRcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args,**kwargs)
                
class Queueoperator(models.Model):
    FirstName    = models.CharField(max_length=50)
    LastName     = models.CharField(max_length=50)
    username     = models.CharField(max_length=50)
    EmailAddress = models.EmailField(max_length=250)
    password     = models.CharField(max_length=50)
    CreatedAt    = models.DateTimeField(auto_now=True)
    Customer     = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Director     = models.ForeignKey(Director, on_delete=models.CASCADE)
    Queue        = models.ManyToManyField(Queue)

class Category(models.Model):
    Name      = models.CharField(max_length=50)
    CreatedAt = models.DateTimeField(auto_now=True)
    Queue     = models.ForeignKey(Queue, on_delete=models.CASCADE)



 
 

