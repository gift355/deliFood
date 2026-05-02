from django.shortcuts import render, get_object_or_404
from .models import FoodItem

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
