from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control bg-white',
            'placeholder': 'Enter your Email'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets ={
            'username': forms.TextInput(attrs={
                'class': 'form-control bg-white',
                'placeholder': 'Enter your username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control bg-white',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control bg-white',
            'placeholder': 'Confirm your password'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

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
        fields = ['default_phone_number', 'default_country', 'default_postcode',
                  'default_town_or_city', 'default_street_address1',
                  'default_street_address2', 'default_county']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['default_phone_number'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Phone number'
        })
        self.fields['default_country'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Phone number'
        })

        self.fields['default_postcode'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Postal Code'
        })
        self.fields['default_town_or_city'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Town or City'
        })
        self.fields['default_street_address1'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Street Address 1'
        })
        self.fields['default_street_address2'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'Street Address 2'
        })
        self.fields['default_county'].widget.attrs.update({
            'class':'form-control bg-dark text-white',
            'placeholder': 'County'
        })
        
