from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import DriverProfileForm

# Create your views here.
@login_required
def register_driver(request):
    # Check if driver has already has a profile
    if hasattr(request.user, 'driver_profile'):
        return redirect('driver dashboard')
    if request.method == 'POST':
        form = DriverProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('driver_dashboard')
    else:
        form = DriverProfileForm()
    return render(request, 'drivers/register_driver.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import DriverProfile

@login_required
def driver_dashboard(request):
    # 1. Get the driver profile (or 404 if they aren't registered as a driver yet)
    # This prevents the page from crashing if a regular user tries to access it
    driver = get_object_or_404(DriverProfile, user=request.user)
    
    # 2. Context dictionary to send data to the HTML
    context = {
        'driver': driver,
        'earnings': driver.total_earnings,
        'status': "Online" if driver.is_online else "Offline",
        # 'active_orders': Order.objects.filter(driver=driver, status='active') # For later!
    }
    
    return render(request, 'drivers/dashboard.html', context)