from django import forms

from inventory.models import Emplacement, Product

class AddEmplacementForm(forms.ModelForm):
    class Meta:
        model = Emplacement
        fields =('city', 'alley', 'row', 'column')

class AddProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ('name','color','size','gender','quantity')





