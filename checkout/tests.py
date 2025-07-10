from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order, OrderLineItem
from products.models import Product, Category
import json

# Create your tests here.
class CheckoutViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        # Create test product with id=1
        self.product = Product.objects.create(
            id=1,
            category=self.category,
            sku='TESTSKU001',
            name='Test Product',
            description='Test product description',
            has_sizes=True,
            price=10.00,
            rating=4.5,
            image_url='http://example.com/image.jpg'
       )
        # Create test user
        self.client = Client()
        self.checkout_url = reverse('checkout:checkout')
        self.order_data = {
           'full_name': 'Jane Doe',
           'email': 'jane@example.com',
           'phone_number': '123456789',
           'country': 'IE',
           'postcode': 'D01 F5P2',
           'town_or_city': 'Dublin',
           'street_address1': '456 main street',
           'street_address2': '',
           'county': 'Dublin',
           'client_secret': 'pi_12345_secret_67890',
       }

    def test_checkout_page_loads(self):
        session = self.client.session
        session['basket'] = {
            '1': {
                'items_by_size': {
                    'M': 1
                } 
            }
        }
        session.save()

        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')

    def test_post_checkout_creates_order(self):
        session = self.client.session
        session['basket'] = {
            '1': {
                'items_by_size': {
                    'M': 1
                } 
            }
        }
        session.save()

        response = self.client.post(self.checkout_url, self.order_data)
        self.assertEqual(response.status_code, 302)

        orders = Order.objects.all()
        self.assertEqual(orders.count(), 1)
        self.assertEqual(orders.first().full_name, 'Jane Doe')

class CheckoutSuccessViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            full_name='Alice',
            email='alice@example.com',
            phone_number='987654321',
            country='IE',
            postcode='D02 F5P2',
            town_or_city='Cork',
            street_address1 = '789 Main Street',
            county='Cork',
            original_basket='{"1": {"quantity": 1, "product_size": "M"}}',
            stripe_pid='test_pid_123'
        )

    def test_checkout_success_page_loads(self):
        response = self.client.get(reverse('checkout:checkout_success', args=[self.order.order_number]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')