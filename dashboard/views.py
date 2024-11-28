from cgitb import html
import os
from django.db.models import Q
from django.template import RequestContext
from django.test import RequestFactory
from order.forms import  CustomerForm, EditOrderForm, NewOrderForm, AddCityForm, OrderItemsForm, PickerForm
from order.models import Cities, Order, OrderItems
from user.models import User
from .forms import ValidateProductForm
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelChoiceField
from inventory.forms import AddEmplacementForm, AddProductForm
from inventory.models import Emplacement, Product
from user.forms import CreateStaffForm

# Create your views here.
@login_required
def dashboard_index(request):
    inc_products = Product.objects.filter(is_disponible=False)
    vendeur_products = Product.objects.filter(vendeur=request.user)
    vendeur_orders = Order.objects.filter(vendeur=request.user)
    delivered_vendeur_orders = Order.objects.filter(vendeur=request.user, status='Delivered')
    returned_vendeur_orders = Order.objects.filter(vendeur=request.user, status='Returned')


    context = {
        'inc_products': inc_products,
        'vendeur_products': vendeur_products,
        'vendeur_orders': vendeur_orders,
        'delivered_vendeur_orders': delivered_vendeur_orders,
        'returned_vendeur_orders': returned_vendeur_orders
    }
    return render(request, 'dashboard/index.html', context)

############## Manager Views #################

@login_required
def add_emplacement(request):
    if request.method == 'POST':
        form = AddEmplacementForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard-index')
    else:
        form = AddEmplacementForm()
    return render(request, 'dashboard/add_emplacement.html', {'form': form})

@login_required
def emplacements(request):
    emplacements= Emplacement.objects.all()
    return render(request, 'dashboard/emplacements.html', {'emplacements': emplacements})

@login_required
def emplacement_details(request, emplacement_pk):
    emplacement = get_object_or_404(Emplacement, id=emplacement_pk)    
    return render(request, 'dashboard/emplacement_details.html', {'emplacement': emplacement})

@login_required
def add_staff(request):
    if request.method == 'POST':
        form = CreateStaffForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('dashboard-index')
    else:
        form = CreateStaffForm()

    return render(request, 'dashboard/add_staff.html', {'form': form})

@login_required
def add_city(request):
    if request.method == 'POST':
        form = AddCityForm(request.POST)
        if form.is_valid():
            city = form.save(commit=False)
            city.city = form.cleaned_data['city'].upper()
            city.save()
            return redirect('cities_list')
    else:
        form = AddCityForm()
    return render(request, 'dashboard/add_city.html', {'form': form})

@login_required
def cities_list(request):
    cities = Cities.objects.all()
    return render(request, 'dashboard/cities_list.html', {'cities': cities})


@login_required
def manager_order_list(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'dashboard/manager/manager_order_list.html', context )

def manager_new_orders(request):
    PickerForm.base_fields['picker'] = ModelChoiceField(queryset=User.objects.filter(role=5))

    return render(request, 'dashboard/manager/new_orders.html',)


def order_pickup(request, order_pk):
    order = Order.objects.get(id=order_pk)
    order_items = OrderItems.objects.filter(order=order)
    PickerForm.base_fields['picker'] = ModelChoiceField(queryset=User.objects.filter(role=5))
    for item in order_items :
        if not item.is_assigned : 
            item.emplacement = item.product.emplacement.address
            if item.emplacement is None :
                item.emplacement = f'NO STORED ITEMS  :  {item.quantity}' 
                item.product.unstored_items -= item.quantity
            elif item.quantity > item.product.stored_items:
                if item.quantity < item.product.unstored_items:
                    item.emplacement =  f'NO STORED ITEMS  :  {item.quantity}' 
                    item.product.unstored_items -= item.quantity
                else: 
                    
                    item.emplacement = f'{item.emplacement} : {item.product.stored_items} .  NO STORED ITEMS : {item.quantity - item.product.stored_items} '
                    item.product.unstored_items -=  item.quantity -item.product.stored_items
                    item.product.emplacement.volume += item.product.volume * item.product.stored_items
                    item.product.stored_items = 0

            else:
                item.emplacement = item.product.emplacement.address
                item.product.stored_items -= item.quantity
                item.product.emplacement.volume += item.product.volume * item.quantity
            item.is_assigned = True
            item.save()
            item.product.save()
            item.product.emplacement.save()
    if request.method == 'POST':
        form = PickerForm(request.POST)
        if form.is_valid():
            order.picker =  User.objects.get(id=form.data['picker'])
            order.status = 'Processing'
            order.save()
            return redirect('manager-new-orders')
    else : 
        form = PickerForm()
    context = {
        'order': order,
        'order_items': order_items,
        'form': form,
    }
    return render(request, 'dashboard/manager/order_pickup.html', context)


###########Receiver Views ##################

@login_required
def product_validation(request, pk):
    product = get_object_or_404(Product, id=pk)  

    if request.method == 'POST':
        form = ValidateProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.volume = form.cleaned_data['longueur'] * form.cleaned_data['largeur'] * form.cleaned_data['hauteur']
            product.is_disponible = True 
            if product.quantity > 30 :
                product.stored_items = 30
                product.unstored_items = product.quantity - product.stored_items
            else : 
                product.stored_items = product.quantity
            
            stored_products_volume = product.volume * product.stored_items
            emplacements = Emplacement.objects.filter(volume__gt = stored_products_volume ).order_by('volume')
            if emplacements :
                emplacement = emplacements.first()
                product.emplacement = emplacement
                emplacement.volume -= stored_products_volume 
            
            else:
                emplacement =  Emplacement.objects.all().order_by('-volume').first()
                products_to_store = emplacement.volume // product.volume
                if products_to_store > 0:
                    product.unstored_items += product.stored_items - products_to_store
                    product.stored_items = products_to_store
                    stored_products_volume = product.volume * product.stored_items
                    emplacement.volume -= stored_products_volume
                    product.emplacement = emplacement
                    
                else: 
        
                    product.stored_items = 0
                    product.unstored_items = product.quantity
                    print("CAN'T Find a place" )
                    
            product.save()
            emplacement.save()
            return redirect('print-barcode',  product_pk = product.id)
    else:
        form = ValidateProductForm(instance=product,)

    context = {
        'product': product,
        'form': form
        }
    return render(request, 'dashboard/receiver/product_validation.html', context)

@login_required
def product_barcode(request, product_pk):
    product = get_object_or_404(Product, id=product_pk)
    return render(request, 'dashboard/receiver/product_barcode.html',{'product': product})



########## Veundeur Views ##################

@login_required
def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)       
        if form.is_valid():
            product=form.save(commit=False)
            product.vendeur = request.user 
            product.set_variation(form) 
            product.set_barcode()
            product.save()
            return redirect('product-detail', product.id)
    else:
        form = AddProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form,})

@login_required
def product_list(request):    
    products = Product.objects.filter(vendeur=request.user)
    return render(request, 'dashboard/product_list.html', {'products': products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    context = {
        'product': product,                
    }
    return render(request, 'dashboard/product_detail.html', context)

@login_required
def add_order(request):
    disponible_products = Product.objects.filter(vendeur=request.user, is_disponible=True)
    if request.method == 'POST': 
        NewOrderForm.base_fields['product'] = ModelChoiceField(queryset=Product.objects.filter(vendeur=request.user, is_disponible=True))
        order_form = NewOrderForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if order_form.is_valid() and customer_form.is_valid():
            order = order_form.save(commit=False)  
            customer = customer_form.save(commit=False)
            if order_form.cleaned_data['quantity'] > Product.objects.get(id=order_form.data['product']).quantity:
                messages.error(request, 'This quantity is not available, please check your inventory')
                return redirect('add-order')
            order.vendeur = request.user
            order.customer = customer                       
            customer.save()
            order.save()
            order.product.add(order_form.data['product'])
            order_item = OrderItems.objects.get(order=order)
            order_item.quantity = order_form.cleaned_data['quantity']      
            order_item.item_price = order_form.cleaned_data['price']
            order_item.save()
            return redirect('order-validation',pk=order.id )

    else : 
        NewOrderForm.base_fields['product'] = ModelChoiceField(queryset=Product.objects.filter(vendeur=request.user, is_disponible=True))
        order_form = NewOrderForm()
        customer_form = CustomerForm()
        
    context = {
        'order_form': order_form,
        'customer_form': customer_form,
        'disponible_products': disponible_products,
        
    }

    return render(request, 'dashboard/add_order.html', context)

@login_required
def order_add_product(request, pk):
    order = Order.objects.get(id=pk)
    
    if request.method == 'POST':
        NewOrderForm.base_fields['product'] = ModelChoiceField(queryset=Product.objects.filter(vendeur=request.user, is_disponible=True))
        order_form = NewOrderForm(request.POST, )
        if order_form.is_valid() :
            order_form.save(commit=False)
            product = Product.objects.get(id=order_form.data['product'])
            if product in order.product.all():
                messages.error(request,f'{product.name} is already in your order, please select an other product')
                return redirect('order-add-product', pk=order.id)
            if order_form.cleaned_data['quantity'] > Product.objects.get(id=order_form.data['product']).quantity:
                messages.error(request, 'This quantity is not available, please check your inventory')
                return redirect('order-add-product', pk=order.id)
            
            order.product.add(order_form.data['product'])
            order_item = OrderItems.objects.get(order=order,product=product)
            order_item.quantity = order_form.cleaned_data['quantity']      
            order_item.item_price = order_form.cleaned_data['price']
            order_item.save()
            return redirect('order-validation',pk=order.id )

    else: 
        NewOrderForm.base_fields['product'] = ModelChoiceField(queryset=Product.objects.filter(vendeur=request.user, is_disponible=True))
        order_form = NewOrderForm()
    
    context = {
        'order_form': order_form,
        'order': order,
    }

    return render(request, 'dashboard/order_add_product.html', context)

@login_required
def orders_list(request):
    if request.GET.get('status') :
        orders = Order.objects.filter(vendeur=request.user, status=request.GET.get('status'))
    else:
        orders = Order.objects.filter(vendeur=request.user)
    return render(request, 'dashboard/orders.html', {'orders': orders})

@login_required
def order_validation(request, pk):
    order = Order.objects.get(id=pk)
    order_items = OrderItems.objects.filter(order=order)
    order.order_amount = 0
    order.order_fees = 0
    
    for item in order_items:
        order.order_amount += item.quantity * item.item_price
        order.order_fees += item.quantity * 5
        order.total = order.order_amount + order.order_fees
        order.save()
    if request.method == 'POST':
        for product in order.product.all():
            quantity = OrderItems.objects.get(order=order, product=product).quantity 
            product.quantity -= quantity
            product.check_disponibility()
            product.save()
        order.status = 'Created'
         
        order.save() 
        messages.success(request, f'Your order has been added succefully !')
        return redirect('orders-list')  
    context =  {
        'order_items': order_items,
         'order': order,
         
         }
    return render(request,'dashboard/order_validation.html', context)

@login_required
def order_edit(request, order_pk, item_pk):
    
    order = Order.objects.get(id=order_pk)
    item = OrderItems.objects.get(order=order, product_id=item_pk) 
    initial_dict = {
        "product" :order.product.get(id=item.product_id) ,
        "price" : item.item_price,
        "quantity":item.quantity
    }
    EditOrderForm.base_fields['product'] = ModelChoiceField(queryset=Product.objects.filter(vendeur=request.user, is_disponible=True))

    if request.method == 'POST':
        order_form = EditOrderForm(request.POST, initial= initial_dict)
        if order_form.is_valid():

            product = Product.objects.get(id=order_form.data['product'])
            if product in order.product.all().exclude(id=item.product_id):
                messages.error(request,f'{product.name} is already in your order, please select an other product')
                return redirect('order-edit', order_pk=order.id, item_pk= item.product.id)
            if order_form.cleaned_data['quantity'] > Product.objects.get(id=order_form.data['product']).quantity:
                messages.error(request, 'This quantity is not available, please check your inventory')
                return redirect('order-edit', order_pk=order.id, item_pk= item.product.id)

            item.product = order_form.cleaned_data['product'] 
            item.item_price = order_form.cleaned_data['price']
            item.quantity = order_form.cleaned_data['quantity']
            
            
            item.save()
            return redirect ('order-validation', pk=order.id)  
                                
    else:
        order_form = EditOrderForm(initial= initial_dict)
      
    context = {
        'order_form': order_form,
        # 'order_item_form': order_item_form,
        'order': order,
        'item': item, 
    }
    return render(request, 'dashboard/order_edit.html', context)

@login_required
def order_item_delete(request, order_pk, item_pk):
    order = Order.objects.get(id=order_pk)
    item = OrderItems.objects.get(order=order, product_id=item_pk) 
    if request.method == 'POST':
        item.delete()
        return redirect('order-validation', pk = order.id )

    return render(request, 'dashboard/order_item_delete.html')

@login_required
def order_delete(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('orders-list')
    return render(request, 'dashboard/order_delete.html')

