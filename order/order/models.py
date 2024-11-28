
from django.db import models
from inventory.models import Emplacement, Product
from user.models import User

# Create your models here.
ORDER_STATUS = (
    ("Created", "Created"),
    ("Processing", "Processing"),
    ("Reported", "Reported"),
    ("Canceled", "Canceled"),
    ("Delivered", "Delivered"),
    ("No answer","No answer"),
    ("Returned", "Returned"),
    ("Out for delivery","Out for delivery")
)

class Cities(models.Model):
    city = models.CharField(max_length=30, unique=True)
    cost = models.PositiveIntegerField()

    def __str__(self):
        return self.city.capitalize()



class Customer(models.Model):
    full_name = models.CharField(max_length=60, verbose_name='full name')
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.full_name


class Order(models.Model):
    product = models.ManyToManyField(Product, through='OrderItems' )
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vendeur')
    picker = models.ForeignKey(User, on_delete=models.CASCADE,  null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.TextField(choices=ORDER_STATUS, default='')
    order_fees = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True)
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total', default=0, null=True)




    def __str__(self):
        return f'Order N° {self.id}'


class OrderItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)    
    item_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='price', null=True)
    quantity = models.PositiveIntegerField(null=True)
    emplacement = models.CharField(max_length=255, null=True)
    is_assigned = models.BooleanField(default=False)



    
    def __str__(self):
        return f'Order N° {self.order.id}-{self.product.id}'
    

class OrderPickUp(models.Model):
    order = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    emplacement =models.CharField(max_length=255)
    pick_quantity = models.PositiveIntegerField()

