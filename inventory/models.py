import random
import string
from django.db import models
from user.models import User
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
# Create your models here.

class Emplacement(models.Model):
    city = models.CharField(max_length=55)
    alley = models.CharField(max_length=3)
    row = models.CharField(max_length=3)
    column = models.CharField(max_length=3)
    address = models.CharField(max_length=25, blank=True)
    volume = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # products = models.ManyToManyField('Product',through='emplacementProduct', blank=True)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        self.address = f'{self.city[0:3].upper()}-{self.alley}-{self.row}-{self.column}'        
        return super().save(*args, **kwargs)

   


class Product(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length= 20, blank=True, null=True)
    size = models.CharField(max_length= 15, blank=True, null=True)
    gender = models.CharField(max_length= 15, blank=True, null=True)
    quantity = models.PositiveIntegerField()
    vendeur = models.ForeignKey(User, on_delete=models.CASCADE)
    is_disponible = models.BooleanField(default=False)
    volume = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    sku = models.CharField(max_length=255, null=True, unique=True)
    barcode = models.ImageField(upload_to="products/codes/", null=True)
    unstored_items = models.PositiveIntegerField(null=True)
    emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE, null=True)
    stored_items = models.IntegerField(null=True)
    unstored_items = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    def set_barcode(self):
        sku_list = Product.objects.values_list('sku', flat=True)
        self.sku = f'{self.vendeur.id}-{self.name[0:4].upper()}-{self.color[0:3].upper()}-{self.size}-{self.gender[0]}' 
        if self.sku in sku_list:
            additional =''.join(random.choices(string.ascii_uppercase, k = 6))
            self.sku += additional
        barcode_writer = ImageWriter()
        ean = barcode.codex.Code39( self.sku, barcode_writer,  add_checksum=False)        
        buffer = BytesIO()
        ean.write(buffer)
        self.barcode.save('barecode.png', File(buffer))

    def set_variation(self, form):

        if form.cleaned_data['color']:
            self.color = form.cleaned_data['color']
        else:
            self.color = 'unicolor'

        if form.cleaned_data['size']:
            self.size = form.cleaned_data['size']
        else:
            self.size = 'standard'

        if form.cleaned_data['gender']:
            self.gender = form.cleaned_data['gender']
        else:
            self.gender = 'uni'

    def check_disponibility(self):
        if self.quantity == 0:
            self.is_disponible = False
 

# class emplacementProduct(models.Model):
#     emplacement = models.ForeignKey(Emplacement, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     items = models.IntegerField(null=True, default=0)

