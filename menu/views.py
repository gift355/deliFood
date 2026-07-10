from django.shortcuts import render,redirect, get_object_or_404
from .models import FoodItem
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from restaurant.models import Restaurant
from .models import FoodItem
from .forms import FoodItemForm

def food_detail(request, pk):
    """
    Displays the full details for a single food item.
    The 'pk' (Primary Key) is passed from the URL when a user clicks a card.
    """
    item = get_object_or_404(FoodItem, pk=pk, available=True)
    
    # Optional: Get related items from the same category to show at the bottom
    related_items = FoodItem.objects.filter(
        category=item.category, 
        available=True
    ).exclude(pk=pk)[:3]

    context = {
        'item': item,
        'related_items': related_items,
    }
    return render(request, 'menu/food_detail.html', context)

def food_list(request):
    """
    A backup view to list all available meals if 
    you ever want a dedicated /menu/ page.
    """
    items = FoodItem.objects.filter(available=True)
    return render(request, 'menu/food_list.html', {'items': items})

# 1. CREATE (Add Food Item)
@login_required
def food_create(request, restaurant_slug):
    # Fetch the restaurant and ensure the logged-in user owns it
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
    if restaurant.vendor_owner != request.user:
        messages.error(request, "Access denied. You do not own this restaurant.")
        return redirect('restaurant:restaurant_dashboard')

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES)
        if form.is_valid():
            food_item = form.save(commit=False)
            food_item.restaurant = restaurant  # Link it to this restaurant automatically
            food_item.save()
            messages.success(request, f"'{food_item.name}' has been added to your menu!")
            return redirect('restaurant:restaurant_dashboard')
    else:
        form = FoodItemForm()
    
    return render(request, 'menu/food_form.html', {
        'form': form, 
        'restaurant': restaurant, 
        'action': 'Add New'
    })

# 2. UPDATE / EDIT (Edit Food Item)
@login_required
def food_update(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    
    # Check permissions against the parent restaurant's owner
    if food_item.restaurant.vendor_owner != request.user:
        messages.error(request, "Access denied. You cannot manage this menu item.")
        return redirect('restaurant:restaurant_dashboard')

    if request.method == 'POST':
        form = FoodItemForm(request.POST, request.FILES, instance=food_item)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{food_item.name}' has been updated.")
            return redirect('restaurant:restaurant_dashboard', )
    else:
        form = FoodItemForm(instance=food_item)
        
    return render(request, 'menu/food_form.html', {
        'form': form, 
        'restaurant': food_item.restaurant, 
        'action': 'Edit'
    })

# 3. DELETE (Remove Food Item)
@login_required
def food_delete(request, pk):
    food_item = get_object_or_404(FoodItem, pk=pk)
    restaurant = food_item.restaurant
    
    if restaurant.vendor_owner != request.user:
        messages.error(request, "Access denied.")
        return redirect('restaurant:restaurant_dashboard')

    if request.method == 'POST':
        food_item.delete()
        messages.warning(request, f"'{food_item.name}' has been removed from your menu.")
        return redirect('restaurant:restaurant_dashboard')
        
    return render(request, 'menu/food_confirm_delete.html', {'food_item': food_item})