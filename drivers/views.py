from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from .forms import DriverProfileForm
from .models import DriverProfile, Transaction
from orders.models import Order
from delivery.models import Delivery


# Create your views here.
@login_required
def register_driver(request):
    # 1. Try to get an existing profile for this user
    # If it exists, we update it. If not, we create a new one.
    try:
        instance = request.user.driverprofile # Note: check if your related_name is 'driver_profile' or 'driverprofile'
    except DriverProfile.DoesNotExist:
        instance = None

    # 2. If they already have a profile AND it's fully filled out, skip to dashboard
    if instance and instance.vehicle_type and instance.license_plate:
        return redirect('driver_dashboard')

    if request.method == 'POST':
        # 3. Pass the 'instance' to the form so Django knows to UPDATE instead of CREATE
        form = DriverProfileForm(request.POST, instance=instance)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('driver_dashboard')
    else:
        form = DriverProfileForm(instance=instance)

    return render(request, 'drivers/register_driver.html', {
        'form': form,
        'full_name': f"{request.user.first_name} {request.user.last_name}"
    })




@login_required
def driver_dashboard(request):
    # 1. Get the driver profile (or 404 if they aren't registered as a driver yet)
    # This prevents the page from crashing if a regular user tries to access it
    driver = get_object_or_404(DriverProfile, user=request.user)

    #Fetch orders from the market place
    available_orders = Order.objects.filter(status='pending', driver__isnull=True).order_by('-created_at')

    #Fetch orders currrently assugned to the driver
    active_orders = Order.objects.filter(driver=driver,status__in=['assigned', 'picked_up']).order_by('-updated_at')
    total_deliveries = Order.objects.filter(driver=driver, status='completed').count()

    
    # 2. Context dictionary to send data to the HTML
    context = {
        'driver': driver,
        'driver_balance': driver.total_earnings,
        'total_deliveries': 0,
        'rating': 5.0,
        'available_orders': [],
        'status': "Online" if driver.is_online else "Offline",
        # 'active_orders': Order.objects.filter(driver=driver, status='active') # For later!
    }
    
    return render(request, 'drivers/driver_dashboard.html', context)

def driver_earnings(request):
    # Try to get the profile, or set it to None
    driver = getattr(request.user, 'driverprofile', None)

    if not driver:
        # If they aren't a driver, send them away or show an error
        return redirect('home')
    transactions = Transaction.objects.filter(driver=request.user.driverprofile).order_by('timestamp')
    last_seven_days = timezone.now() - timedelta(days=7)
    weekly_data = transactions.filter(timestamp__gte=last_seven_days).aggregate(Sum('amount'))
    weekly_total = weekly_data['amount__sum'] or 0
    context = {
        'transactions': transactions,
        'weekly_total': weekly_total,
        'wallet_balance': driver.total_earnings
    }

    return render(request, 'drivers/driver_earnings.html', context)

@login_required
def my_deliveries(request):
    driver = get_object_or_404(DriverProfile, user=request.user)
    
    # We query the ORDER model because that's what you're using in Admin
    active_orders = Order.objects.filter(
        driver=driver,
        status__in=['assigned', 'picked_up'] # Only show active work
    ).prefetch_related('items__food_item__restaurant').order_by('-updated_at')
    
    context = {
        'orders': active_orders,
        'active_count': active_orders.count(),
        'driver': driver,
    }
    
    return render(request, 'drivers/my_deliveries.html', context)