from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Order

def update_order_status(request, order_id, new_status):
    # 1. Get the order and verify the logged-in driver owns it
    order = get_object_or_404(Order, id=order_id, driver__user=request.user)
    
    # 2. Handle 'Picked Up' (Moving from restaurant to customer)
    if new_status == 'picked_up':
        order.status = 'picked_up'
        order.save()
        messages.info(request, f"Order #{order.order_number} picked up. Drive safe!")

    # 3. Handle 'Completed' (The delivery is done, time to pay!)
    elif new_status == 'completed':
        order.status = 'completed'
        order.save()
        
        # Add the payout to the driver's total earnings
        driver = order.driver
        driver.total_earnings += order.payout_amount
        driver.save()
        
        messages.success(request, f"Delivery finished! ₦{order.payout_amount} added to your wallet.")

    return redirect('my_deliveries')

@login_required
def order_detail(request, order_number):
    # Fetch the order using the unique order_number field
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
    }
    return render(request, 'orders/order_detail.html', context)