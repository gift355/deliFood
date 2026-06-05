from django.db import models
from django.conf import settings
from orders.models import Order

# Create your models here.
class Transaction(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('successful', 'Successful'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('transfer', 'Bank Transfer'),
        ('wallet', 'Digital Wallet')
    ]
    #core relationship
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')

    # Security & Gateway Tracking Fields
    # Storing the unique tracking reference provided by Stripe Paystack (ref_xxxx)
    payment_reference = models.CharField(max_length=100, unique=True, db_index=True)
    payment_gateway = models.CharField(max_length=50, default='paystack') # or 'stripe'
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='card')

    # Financial Auditing Fields
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='NGN') # Change to 'USD', 'ZAR', etc. if needed
    
    # Operational Status Checks
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='initiated')
    gateway_response = models.JSONField(null=True, blank=True) # Stores raw response logs for debug safety
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Txn {self.payment_reference} - {self.amount} {self.currency} ({self.status})"

