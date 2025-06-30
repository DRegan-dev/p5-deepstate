from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from basket.contexts import basket_contents
from .forms import OrderForm
import json

# Create your views here.
def checkout(request):
    """ Display the checkout page """
    basket = basket_contents(request)
    order_form = OrderForm()

    basket_items = []
    for item in basket.get('basket_items', []):
        item_data = {
            'product': item['product'],
            'quantity': item['quantity'],
            'price': item['product'].price,
            'total': item['product'].price * item['quantity'],
        }
        basket_items.append(item_data)

    context = {
        'order_form': order_form,
        'basket_items': basket_items,
        'total': basket.get('total', 0),
        'product_count': basket.get('product_count', 0),
        'delivery': basket.get('delivery', 0),
        'grand_total': basket.get('grand_total', 0)
    }

    return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_number):
    """ Handle successful checkout """
    context = {
        'order_number': order_number,
    }
    return render(request, 'checkout/checkout_success.html', context)

@require_POST
def cache_checkout_data(request):
    """Cache checkout data for Stripe"""
    try:
        data = json.loads(request.body)
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=400)
    
@csrf_exempt
@require_POST
def stripe_webhook(request):
    return HttpResponse(status=200)