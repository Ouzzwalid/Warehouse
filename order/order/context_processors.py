from .models import Order

def created_orders(request):
    return {
        'created_orders' : Order.objects.filter(status='Created')
    }