from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from checkout.models import Order
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm




# Create your views here.
def login_view(request):
    if request.method == 'POST':
        print(f"=== POST DATA ===")
        print(f"Raw POST data: {request.POST}")
        form = UserLoginForm(data=request.POST)
        
        print(f'Form errors: {form.errors}')

        if form.is_valid():
            print("Form is valid atempting login")
            print(f'Form data: { form.cleaned_data if form.is_bound else "Not Bound"}')
            user = form.get_user()
            login(request, user)
            print(f"User {user.username} successfully logged in")
            messages.success(request, f"Welcome back, {user.username}")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        print("=== LOGIN GET REQUEST ===")
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        print("=== POST REQUEST RECEEIVED ===")
        print(f"POST data: {request.POST}")

        form = UserRegistrationForm(request.POST)
        print(f"Form is valid: {form.is_valid()}")
        if form.is_valid():
            print('Form is valid - attempting to save user')
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created succesfully!')
            return redirect('home')
        else:
            print(f"Form is NOT valid. Errors: {form.errors}")
            print(f"Form non=field errors: {form.non_field_errors()}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been  logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    """
    Display the user's profile.
    """
    print(f'entered profile view')
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        print(f'post request received')
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            print(f'Profile updated successfully')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'There was an error updating your profile. Please try again')
    else:
        form = UserProfileForm()

    orders = profile.orders.all().order_by('-date')

    template = 'accounts/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

        

