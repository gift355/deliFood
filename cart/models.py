# Create your models here.
from django.db import models
from django.conf import settings
from menu.models import FoodItem
from restaurant.models import Restaurant
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
#from .models import CartItem


class Cart(models.Model):
    # Link to your Custom User model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart'
    )
    
    # Track which restaurant this cart belongs to
    # This helps enforce the "one restaurant per order" rule
    restaurant = models.ForeignKey(
        Restaurant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_price(self):
        """Calculates the total price of all items in the cart."""
        return sum(item.get_cost() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    # Reference to your FoodItem model
    food_item = models.ForeignKey(
        FoodItem, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.food_item.name}"

    def get_cost(self):
        """Price calculation based on your FoodItem price field."""
        return self.food_item.price * self.quantity
    
@login_required
def some_view(request):
    cart_count = CartItem.objects.filter(cart__user=request.user).aggregate(total_qty=Sum('quantity'))['total_qty'] or 0

    return render(request, "home.html", {
        "cart_count": cart_count
    })