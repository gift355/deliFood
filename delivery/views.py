# Create your views here.
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Delivery
from django.utils import timezone

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
def pickup_delivery(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk, driver=request.user.driverprofile)
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
def complete_delivery(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk, driver=request.user.driverprofile)
    delivery.status = 'delivered'
    delivery.delivered_at = timezone.now()
    delivery.save()

    # 2. Update Order
    order = delivery.order
    order.status = 'completed' # or 'delivered' depending on your Choice list
    order.save()

    # You could also trigger payment logic here!
    messages.success(request, "Delivery complete! Great job.")
    return redirect('my_deliveries')