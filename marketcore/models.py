from django.db import models
import os
from django.conf import settings
from datetime import datetime

class User(models.Model):
    username = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    register_at = models.DateTimeField(default=datetime.now, blank=True);

    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username;

    def add(self,name,password):

        self.objects.create(username= name, password= password);

    class Meta:
        verbose_name_plural = 'User'

class Type(models.Model):
    name = models.CharField(max_length = 400)

    def __str__(self):
        return self.name;
    class Meta:
        verbose_name_plural = 'Type'

class Product(models.Model):

    name = models.CharField(max_length = 500)
    type = models.ForeignKey(Type,null=True,related_name='Type',on_delete=models.SET_NULL)
    description = models.TextField()
    QUALITY_CHOICES = (
        ('NEW','NEW'),
        ('US_P','USED_PERFECT'),
        ('US_M','USED_MINIMAL'),
        ('USED','USED'),
        ('BROKE','BROKe'),
    )
    quality = models.CharField(max_length=50, choices=QUALITY_CHOICES,default='NEW')
    image = models.ImageField(upload_to ='imgs/',default='static/products_imgs/noname/nn.jpg')
    seller = models.ForeignKey(User,null=True,related_name='Owner', on_delete=models.SET_NULL);
    price = models.DecimalField(max_digits=10,decimal_places=2);
    buyer = models.ForeignKey(User,blank=True, null=True,related_name='Buyer', on_delete=models.SET_NULL);
    added_at = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name;



    class Meta:
        verbose_name_plural = 'Product'

class Message(models.Model):

    title = models.CharField(max_length= 100)
    content = models.TextField()
    to = models.ForeignKey(User,null=True,related_name='To',on_delete=models.SET_NULL)
    mailer = models.ForeignKey(User,null=True,related_name='From',on_delete=models.SET_NULL)
    send_at = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return self.title;

    class Meta:
        verbose_name_plural = 'Message'

# Create your models here.
