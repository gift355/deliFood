from django.db import models
#from orders.models import Orders
class Delivery(models.Model):
    # Explicit status choices for the logistics side
    STATUS_CHOICES = [
        ("pending", "Pending"),       # Waiting for a driver
        ("assigned", "Assigned"),     # Driver accepted, heading to restaurant
        ("picked_up", "Picked Up"),   # Driver has the food
        ("on_the_way", "On The Way"), # Driver heading to customer
        ("delivered", "Delivered"),   # Mission complete
        ("cancelled", "Cancelled"),   # Mission aborted
    ]

    # The "One-to-One" link: Every Order has exactly one Delivery mission
    order = models.OneToOneField(
        "orders.Order", 
        on_delete=models.CASCADE,
        related_name="delivery_mission"
    )

    # Link to the driver performing the task
    driver = models.ForeignKey(
        "drivers.DriverProfile", 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="delivery_tasks"
    )

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default="pending"
    )

    # Addresses: We copy these from the Order/Restaurant so they are "locked in"
    pickup_address = models.TextField(help_text="Restaurant location")
    dropoff_address = models.TextField(help_text="Customer location")

    # Financials
    delivery_fee = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Amount driver earns for this trip"
    )

    # Time Tracking (Essential for analytics later!)
    assigned_at = models.DateTimeField(null=True, blank=True)
    picked_up_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # This checks if order exists before trying to grab the number
        order_no = self.order.order_number if self.order else "No Order"
        return f"Delivery for Order #{order_no} - {self.status}"