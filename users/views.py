from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomerSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from restaurant.models import Restaurant
from django.db.models import Q
# Create your views here.

def landing_view(request):
    return render(request, 'users/landing.html')

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

#def home_view(request):
    food_items = FoodItem.objects.filter(available=True).order_by('-id')[:12]
    context = {
        'food_items': food_items,
    }
    return render(request, 'users/home.html', context)
def home_view(request):
    # 1. Capture the search inputs from the GET request
    # 'address' matches the name="" attribute in your delivery address bar
    address_query = request.GET.get('address', '').strip()
    # 'q' can be used for a general food/restaurant name search bar
    food_query = request.GET.get('q', '').strip()

    # 2. Start with all available food items
    food_items = FoodItem.objects.filter(available=True, restaurant__is_active=True)

    # 3. Filter by Location (Address/City)
    # This filters food items based on their restaurant's address
    if address_query:
        food_items = food_items.filter(restaurant__address__icontains=address_query)

    # 4. Filter by Food Name or Restaurant Name
    # This allows a user to search for "Pizza" or "Mama Calabar"
    if food_query:
        food_items = food_items.filter(
            Q(name__icontains=food_query) | 
            Q(restaurant__name__icontains=food_query) |
            Q(description__icontains=food_query)
        )

    # 5. Order and Limit (keeping your original 12-item limit)
    food_items = food_items.order_by('-id')[:12]

    context = {
        'food_items': food_items,
        'address_query': address_query,
        'food_query': food_query,
    }
    return render(request, 'users/home.html', context)


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


