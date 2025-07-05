from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib import messages
from basket.contexts import basket_contents
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from accounts.models import UserProfile
from django.conf import settings
import json
import stripe

# Create your views here.
def checkout(request):
    """ Display the checkout page """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        form_data = {
            'full_name': request.POST.get('full_name', ''),
            'email': request.POST.get('email', ''), 
            'phone_number': request.POST.get('phone_number', ''),
            'country': request.POST.get('country', ''),
            'postcode': request.POST.get('postcode', ''),
            'town_or_city': request.POST.get('town_or_city', ''),
            'street_address1': request.POST.get('street_address1', ''),
            'street_address2': request.POST.get('street_address2', ''),
            'county': request.POST.get('county', ''),
        }
    
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.order_number = order.generate_order_number()
            order.original_basket = json.dumps(basket)

            if request.user.is_authenticated:
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                order.user_profile  = profile

            client_secret = request.POST.get('client_secret','')
            order.stripe_pid = client_secret.split('_secret')[0] if '_secret' in client_secret else ''

            order.save()

            for item_id, item_data in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                            lineitem_total=product.price * item_data
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                                lineitem_total=product.price * quantity
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database."
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('basket:view_basket'))
                
            if request.user.is_authenticated and 'save_info' in request.POST:
                profile.default_phone_number = order.phone_number
                profile.default_country=order.country
                profile.default_postcode=order.postcode
                profile.default_town_or_city = order.town_or_city
                profile.default_street_address1 = order.street_address1
                profile.default_street_address2 = order.street_address2
                profile.default_county = order.county
                profile.save()

                
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout:checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. '
                        'Please double check your information.')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))

            
                    
        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount = stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        if not intent or not intent.client_secret:
            messages.error(request, 'Error creating stripe payment intent')
            return redirect(reverse('basket:basket_view'))
        
        order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(request, "Stripe public key is missing. Did you forget to set it in your environment?")

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
            'basket': current_basket,
            'delivery': current_basket['delivery'],
            'grand_total': current_basket['grand_total'],
            'product_count': current_basket['product_count'],
            'basket_items': current_basket['basket_items'],
        }

        return render(request, template, context)

    # for item in basket.get('basket_items', []):
    #     item_data = {
    #         'product': item['product'],
    #         'quantity': item['quantity'],
    #         'price': item['product'].price,
    #         'total': item['product'].price * item['quantity'],
    #     }
    #     basket_items.append(item_data)

    # context = {
    #     'order_form': order_form,
    #     'basket_items': basket_items,
    #     'total': basket.get('total', 0),
    #     'product_count': basket.get('product_count', 0),
    #     'delivery': basket.get('delivery', 0),
    #     'grand_total': basket.get('grand_total', 0),
    #     'stripe_public_key': stripe_public_key,
    #     'client_secret': intent.client_secret,

    # }

    # return render(request, 'checkout/checkout.html', context)

def checkout_success(request, order_number):
    """ Handle successful checkout """

    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')
    
    if 'basket' in request.session:
        del request.session['basket']
    
    template = 'checkout/checkout_success.html'

    context = {
        'order': order,
    }
    return render(request, template, context)

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