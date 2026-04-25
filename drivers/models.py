from django.db import models
from django.conf import settings

# Create your models here.
class DriverProfile(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_online= models.BooleanField(default=False)
    vehicle_type= models.CharField(max_length=50, choices=[('bike', 'Bike'), ('car', 'Car')], default='bike')
    total_earnings= models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    license_plate=models.CharField(max_length=15, blank=True)
    current_location_lat=models.FloatField(null=True, blank=True)
    current_location_lon=models.FloatField(null=True, blank=True)
    ratings=models.DecimalField(max_digits=3, decimal_places=2, default=5.0)

    def __str__(self):
        return f"Driver: {self.user.username} -  Earnings: NGN{self.total_earnings}"
    
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('delivery', 'Delivery Pay'),
        ('bonus', 'Bonus'),
        ('withdrawal', 'Withdrawal'),
    ]

    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='delivery')
    description = models.CharField(max_length=255, blank=True) # e.g., "Order #1024"
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.driver.user.username} - {self.transaction_type} - ₦{self.amount}"