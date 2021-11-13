from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#cada vez que agrege algo necesito hacer python manage.py makemigrations y despues migrate 


class Customer(models.Model):
    # cascade just basically means that whenever a user is
    #deleted we'll go ahead and delete that
    #relationship to that customer
    #one-to-one field means that a user can have one customer and a customer can
    #only have one user
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)#black is para poder crear un customer sin user
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    #para la imagen del profile
    profile_pic = models.ImageField(default='default-profile-pic.jpg',null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True)

    #this is for return the name in the admin data bases
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    #this is for return the name in the admin data bases
    def __str__(self):
        return self.name
        
class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Out Door', 'Out Door'),
        )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices= CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True, null=True)
    tags = models.ManyToManyField(Tag)

    #this is for return the name in the admin data bases
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    


    def __str__(self):
        return self.product.name