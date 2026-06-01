from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RestaurantOnboardingForm
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .models import Restaurant



User = get_user_model()

def restaurant_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == User.Role.RESTAURANT:
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper


@login_required
def restaurant_onboarding(request):
    # If they already managed to upgrade and have a profile, skip onboarding
    if request.user.role == User.Role.RESTAURANT and Restaurant.objects.filter(vendor_owner=request.user).exists():
        return redirect('restaurant_dashboard')

    if request.method == 'POST':
        form = RestaurantOnboardingForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.vendor_owner = request.user
            restaurant.save()
            
            # --- AUTOMATED VENDOR UPGRADE ---
            user_account = request.user
            user_account.role = User.Role.RESTAURANT
            user_account.save()
            
            messages.success(request, f"Congratulations! Your account has been upgraded and '{restaurant.name}' is now live!")
            return redirect('restaurant_dashboard')
    else:
        form = RestaurantOnboardingForm()
        
    return render(request, 'restaurant/restaurant_onboarding.html', {'form': form})


@login_required
@restaurant_required
def restaurant_dashboard(request):
    # Fetch the newly created profile for this upgraded user
    restaurant = get_object_or_404(Restaurant, vendor_owner=request.user)
    
    # Grab all menu items belonging to this restaurant (uses your model's related_name)
    menu_items = restaurant.menu_items.all()
    
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
    }
    return render(request, 'restaurant/dashboard.html', context)

def restaurant_detail(request, slug):
    # Fetching by slug to match your model's unique slug field
    restaurant = get_object_or_404(Restaurant, slug=slug)
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})