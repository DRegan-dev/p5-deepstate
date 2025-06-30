from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from basket.contexts import basket_contents
from .forms import OrderForm
from django.conf import settings
import json
import stripe

# Create your views here.
def checkout(request):
    """ Display the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY
    basket = basket_contents(request)

    order_form = OrderForm()

    basket_items = []
    total = basket['grand_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount = stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, "Stripe public key is missing. Did you forget to set it in your environment?")

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
        'grand_total': basket.get('grand_total', 0),
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,

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