from django.contrib import admin

from .models import Emplacement, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendeur', 'quantity', 'is_disponible')
admin.site.register(Emplacement)
admin.site.register(Product, ProductAdmin )
# admin.site.register(Item)