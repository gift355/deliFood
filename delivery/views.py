# Create your views here.
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Delivery
from drivers.models import DriverProfile
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def accept_delivery(request, pk):
    # Start the atomic transaction
    with transaction.atomic():
        # 'select_for_update' locks this row in the DB until the 'with' block ends
        delivery = Delivery.objects.select_for_update().get(pk=pk)
        
        # Double-check that someone else didn't grab it 0.001s before us
        if delivery.status == 'pending' and delivery.driver is None:
            delivery.driver = request.user.driverprofile
            delivery.status = 'assigned'
            delivery.assigned_at = timezone.now()
            delivery.save()
            messages.success(request, "Order accepted! Get moving!")
        else:
            messages.error(request, "Too late! Another driver already took this one.")
            
    return redirect('driver_dashboard')


# 2. PICKUP
@login_required
def pickup_delivery(request, pk):
    driver_profile = get_object_or_404(DriverProfile, user=request.user)
    
    # 🚀 FIX: Find the delivery tracking row by the order ID first
    delivery = get_object_or_404(Delivery, order__id=pk)
    
    # Secure safety check: If it's already assigned to another driver, stop them
    if delivery.driver and delivery.driver != driver_profile:
        messages.error(request, "This delivery has already been claimed by another driver.")
        return redirect('driver_dashboard')
        
    # Ensure the driver relationship is officially bound to the delivery row
    delivery.driver = driver_profile
    delivery.status = 'picked_up'
    delivery.picked_up_at = timezone.now()
    delivery.save()
    
    # Update the parent order status so customers can track it live
    order = delivery.order
    order.status = 'picked_up'
    order.save()

    messages.success(request, f"Order #{order.order_number} successfully picked up!")
    
    # 🚀 Redirect back to your dashboard (or 'my_deliveries' if registered in core urls)
    return redirect('driver_dashboard')
#def pickup_delivery(request, pk):
    driver_profile = get_object_or_404(DriverProfile, user=request.user)
    delivery = get_object_or_404(Delivery, order__id=pk, driver=driver_profile)
    delivery.status = 'picked_up'
    delivery.picked_up_at = timezone.now()
    delivery.save()
    # Update the order status so it shows up in view
    order = delivery.order
    order.status = 'picked_up'
    order.save()

    messages.success(request, f"Order #{order.order_number} picked up!")
    return redirect('my_deliveries')

# 3. COMPLETE
@login_required
def complete_delivery(request, pk):
    driver_profile = get_object_or_404(DriverProfile, user=request.user)
    delivery = get_object_or_404(Delivery, order__id=pk, driver=driver_profile)
    with transaction.atomic():
        delivery.status = 'delivered'
        delivery.delivered_at = timezone.now()
        delivery.save()

    # 2. Update Order
        order = delivery.order
        order.status = 'completed' # or 'delivered' depending on your Choice list
        order.save()

        # WALLET TOP-UP LOGIC: Add the specific trip fee to the driver's total
        if delivery.delivery_fee:
            driver_profile.total_earnings += delivery.delivery_fee
            driver_profile.save()
            payout_text = f"₦{delivery.delivery_fee}"
        else:
            payout_text = "₦0.00"

    messages.success(request, f"Delivery complete! Great job. {payout_text} added to your balance.")
    return redirect('my_deliveries')

   