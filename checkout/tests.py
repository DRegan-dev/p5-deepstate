from django.test import TestCase Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, OrderLineItem
from products.models import Product
import json

# Create your tests here.
class CheckoutViewsTest(TestCase):
    def setup(self):
        # Create test user
       self.client = Client()
       self.checkout_url = reverse('checkout:checkout')
       self.order_data = {
           'full_name': 'Jane Doe',
           'email': 'jane@example',
           'phone_number': '123456789',
           'country': 'IE',
           'postcode': 'D01 F5P2',
           'town_or_city': 'Dublin',
           'street_address1': '456 main street',
           'street_address2': '',
           'county': 'Dublin',
       }

    def test_checkout_page_loads(self):
        response = self.client.get(self.checkout_url)
        seld.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_post_checkout_creates_order(self):
        session = self.client.session
        session['basket'] = {
            '1': {'quantity': 1, 'product_size': 'M'}
        }
        session.save()

        response = self.client.post(self.checkout_url, self.order_data)
        self.assertEqual(response.status_code, 302)

        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first().full_name, 'Jane Doe')