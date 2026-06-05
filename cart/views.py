# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.utils import timezone
from orders.models import Order, OrderItem
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

@login_required
def place_order(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if not cart.items.exists():
        messages.error(request, "Your cart is empty! Add items before checking out.")
        return redirect('cart_detail')
        
    if request.method == 'POST':
        # Capture the address from your checkout form submission
        address = request.POST.get('delivery_address', '').strip()
        
        # Validation fallback rule so database doesn't reject it
        if not address:
            messages.error(request, "Please provide a delivery address to complete your order.")
            return redirect('cart_detail')
            
        # 1. GENERATE A COMPACT 10-CHARACTER ORDER CODE
        # Using a 3-character prefix + 7 random uppercase characters to fit max_length=10 perfectly
        unique_order_number = f"DL-{get_random_string(7).upper()}"
        
        # 2. CREATE THE MAIN ORDER MATCHING YOUR EXACT FIELDS
        order = Order.objects.create(
            customer=request.user,
            order_number=unique_order_number,
            delivery_address=address,
            total_amount=cart.total_price,
            status='pending', # Matches your default state choice
            payout_amount=500 # Optional: allocating 80% to driver payout
        )
        
        # 3. MIGRATE CART ITEMS TO ORDER ITEMS
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                food_item=cart_item.food_item,
                quantity=cart_item.quantity,
                price=cart_item.food_item.price
            )
            
        # 4. TEAR DOWN ACTIVE CART TRACKING ENTRIES
        cart.items.all().delete()
        cart.restaurant = None
        cart.save()
        
        # 5. STREAM TO SECURE PAYMENT FRAMEWORK
        return redirect('payments:initiate_payment', order_number=order.order_number)

    return render(request, 'cart/cart_detail.html', {'cart': cart})
