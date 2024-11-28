from django import forms

from inventory.models import  Product

class ValidateProductForm(forms.ModelForm):
    longueur =  forms.IntegerField()
    largeur =  forms.IntegerField()
    hauteur =  forms.IntegerField()
    class Meta:
        model = Product
        fields = ('name','color','size','gender','longueur','largeur','hauteur','quantity',)