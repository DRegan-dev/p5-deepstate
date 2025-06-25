from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.Post.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user in not None:
            login(request, user)
            messages.success(request, 'Succesfully logged in!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.method == 'POST':
        FORM = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created succesfully!')
            return redirect('home')
    else:
        form = UserCreationForm

    return render(request, 'account/register.html', {'form': form})