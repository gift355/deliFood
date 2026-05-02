
from django.shortcuts import render, get_object_or_404
from .models import Restaurant

def restaurant_detail(request, slug):
    # Fetching by slug to match your model's unique slug field
    restaurant = get_object_or_404(Restaurant, slug=slug)
    return render(request, 'restaurant/restaurant_detail.html', {'restaurant': restaurant})