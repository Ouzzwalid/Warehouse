from django import forms

from inventory.models import Product 
from .models import Cities, Customer, Order, OrderItems


class OrderItemsForm(forms.ModelForm):
    class Meta:
        model = OrderItems
        fields = ('quantity', 'item_price')
        
        
class NewOrderForm(forms.ModelForm):
    price = forms.DecimalField()
    quantity = forms.IntegerField()
    class Meta:
        model = Order
        fields = ('product','price', 'quantity')
    
    # def __init__(self, *args, **kargs):
    #     super().__init__(*args, **kargs)
    #     self.fields['product'].queryset = Product.objects.filter(vendeur=self.fields['vendeur']) 

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class AddCityForm(forms.ModelForm):
    class Meta:
        model = Cities
        fields = '__all__'

class BlankForm(forms.Form):
    name = forms.CharField(widget=forms.HiddenInput(), required=False)


class EditOrderForm(forms.Form):
    product =  forms.CharField()
    price = forms.DecimalField()
    quantity = forms.IntegerField()

class PickerForm(forms.Form):
    picker = forms.CharField()


