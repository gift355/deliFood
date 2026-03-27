from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomerSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, 'users/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Log in the user immediately after thhey signup
            login(request, user)
            return redirect('home')
    else:
        form = CustomerSignupForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        # 1. Capture the data from the login form
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # 2. Get the validated username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # 3. Check if this user exists in the database (Authentication)
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # 4. Start the session (Login)
                login(request, user)
                return redirect('home') # Go to home page
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "Invalid Credentials")
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})



