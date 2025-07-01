from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your Email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your Password'
        })

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your Username'
        })

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs)
        """
        Add paceholders and classes, remove auto-generated labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality'
        }

        self.fields['default_phone_number'].widget.attrs['autofocus']= True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
