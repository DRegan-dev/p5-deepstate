from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Category

# Create your tests here.
class BasketTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            id=1,
            category=self.category,
            sku='SKU123',
            name='Test Product',
            price=10.00,
            rating=2
        )
        self.add_url = reverse('basket:add_to_basket', args=[self.product.id])
        self.view_url = reverse('basket:view_basket')
        self.remove_url = reverse('basket:remove_from_basket', args=[self.product.id])

    def test_add_item_to_basket(self):
        response = self.client.post(self.add_url, {'quantity': 2, 'product_size': 'M'})
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn(str(self.product.id), session['basket'])
        self.assertEqual(session['basket'][str(self.product.id)]['items_by_size']['M'], 2)

    def test_update_item_quantity(self):
        response = self.client.post(self.add_url, {
            'quantity': 2,
            'product_size': 'M'        
        })

        session = self.client.session
        self.assertEqual(session['basket'][str(self.product.id)]['items_by_size']['M'], 2)
        
        response = self.client.post(self.add_url, {
            'quantity': 2,
            'product_size': 'M'
        })

        session = self.client.session
        self.assertEqual(session['basket'][str(self.product.id)]['items_by_size']['M'], 4)

    def test_remove_item_from_basket(self):
        self.client.post(self.add_url, {'quantity': 1, 'product_size': 'M'})
        response = self.client.post(self.remove_url)
        self.assertEqual(response.status_code, 200)
        session = self.client.session
        self.assertNotIn(str(self.product.id), session.get('basket', {}))

    def test_view_basket_page(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'basket/basket.html')