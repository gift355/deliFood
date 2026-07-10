from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .forms import RestaurantOnboardingForm
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .models import Restaurant
from users.models import User
from orders.models import OrderItem



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
        return redirect('restaurant:restaurant_dashboard')

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
            return redirect('restaurant:restaurant_dashboard')
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
    #Find all completed order that features  this restaurant's dishes
    completed_restaurant_items =OrderItem.objects.filter(food_item__restaurant=restaurant,order__status='completed')
    total_earnings = 0
    for item in completed_restaurant_items:
        total_earnings += item.price * item.quantity

    
    completed_orders_count = completed_restaurant_items.values('order').distinct().count()
    
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'total_earnings': total_earnings,
        'completed_orders_count': completed_orders_count
    }
    return render(request, 'restaurant/restaurant_dashboard.html', context)

def restaurant_detail(request, slug):
    # Fetching by slug to match your model's unique slug field
    restaurant = get_object_or_404(Restaurant, slug=slug)
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})


@login_required
def restaurant_update(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    
    # Security Check: Ensure only the owner can modify this restaurant
    if restaurant.vendor_owner != request.user:
        messages.error(request, "You do not have permission to edit this restaurant.")
        return redirect('restaurant:restaurant_detail', slug=restaurant.slug)

    if request.method == 'POST':
        form = RestaurantOnboardingForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{restaurant.name}' details updated successfully!")
            return redirect('restaurant:restaurant_detail', slug=restaurant.slug)
    else:
        form = RestaurantOnboardingForm(instance=restaurant)
        
    # We reuse your onboarding template for updating to save work!
    return render(request, 'restaurant/restaurant_onboarding.html', {
        'form': form, 
        'action': 'Update', 
        'restaurant': restaurant
    })


# 4. DELETE (Remove restaurant from the platform)
@login_required
def restaurant_delete(request, slug):
    restaurant = get_object_or_404(Restaurant, slug=slug)
    
    # Security Check: Ensure only the owner can delete it
    if restaurant.vendor_owner != request.user:
        messages.error(request, "You do not have permission to delete this restaurant.")
        return redirect('restaurant:restaurant_detail', slug=restaurant.slug)

    if request.method == 'POST':
        restaurant.delete()
        messages.warning(request, f"'{restaurant.name}' has been successfully removed.")
        return redirect('restaurant:restaurant_list')
        
    return render(request, 'restaurant/restaurant_confirm_delete.html', {'restaurant': restaurant})