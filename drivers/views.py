from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import DriverProfileForm
from .models import DriverProfile

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