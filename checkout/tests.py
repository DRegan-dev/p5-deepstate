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
        self.user - User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.product = Product.objects.create(
            name='Test Product',
            description ='Test Product',
            price = 10.00,
            sku='TESTSKU'
        )

        self.order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='US',
            postcode=12345,
            town_or_city='Test City',
            street_address1= '123 Test St'
            stripe_pid='pid_test'
        )

        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            lineitem_total=20.00
        )

        self.client = Client()