# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from menu.models import FoodItem
from .models import Cart, CartItem

@login_required
def add_to_cart(request, item_id):
    food_item = get_object_or_404(FoodItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # 1. Check if the user is switching restaurants
    if cart.restaurant and cart.restaurant != food_item.restaurant:
        messages.error(request, f"You can only order from {cart.restaurant.name} right now. Clear your cart to order from a different restaurant.")
        return redirect('home')

    # 2. Set the restaurant if the cart was empty
    if not cart.restaurant:
        cart.restaurant = food_item.restaurant
        cart.save()

    # 3. NEW: Get the quantity from the POST form
    # We use .get('quantity', 1) as a fallback just in case
    qty_from_form = request.POST.get('quantity', 1)
    
    try:
        quantity = int(qty_from_form)
    except ValueError:
        quantity = 1 # Fallback if someone enters something weird

    # 4. Get or create the specific item in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, food_item=food_item)
    
    if not item_created:
        # If it's already there, ADD the new quantity to the existing one
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"Updated quantity for {food_item.name}.")
    else:
        # If it's new, set the quantity to exactly what they picked
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f"Added {quantity} x {food_item.name} to your cart.")

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    # Retrieve the user's cart or return an empty state
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = cart_item.cart
    cart_item.delete()

    # If the cart is now empty, reset the restaurant
    if not cart.items.exists():
        cart.restaurant = None
        cart.save()

    messages.info(request, "Item removed from cart.")
    return redirect('cart_detail')
