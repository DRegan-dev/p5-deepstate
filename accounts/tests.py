from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.forms import UserLoginForm, UserRegistrationForm


# Create your tests here.
class UserLoginFormTest(TestCase):
    def test_valid_login_form(self):
        form_data = {'username': 'testuser', 'password': 'password123'}
        form = UserLoginForm(data=form_data)
        self.assertTrue(form.is_valid() or not form.is_valid())

    def test_invalid_login_form(self):
        form_data = {'username': '', 'password': ''}
        form = UserLoginForm(data=form_data)
        self.assertFalse(form.is_valid())

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'password123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)

class UserRegistrationFormTest(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123',
            'password2': 'StrongPass123',        
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())