from django.db import models

class FoodItem(models.Model):
    # These choices align with your requirement for 4 main categories
    CATEGORY_CHOICES = [
        ('local_dish', 'Local Dish'),
        ('fast_food', 'Fast Food'),
        ('drinks', 'Drinks'),
        ('desserts', 'Desserts'),
    ]

    # Links perfectly to the Restaurant model you just chose
    restaurant = models.ForeignKey(
        'restaurant.Restaurant', 
        on_delete=models.CASCADE, 
        related_name='menu_items'
    )
    
    name = models.CharField(max_length=100)
    description = models.TextField(help_text="e.g., Spicy Jollof Rice with Fried Chicken")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='food_items/')
    
    # Dropdown for the 4 categories
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='local_dish'
    )
    
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"