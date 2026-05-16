from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from delivery.models import Delivery

@receiver(post_save, sender=Order)
def create_delivery_for_new_order(sender, instance, created, **kwargs):
    if created:
        # This code runs only when a NEW order is created
        Delivery.objects.create(
            order=instance,
            pickup_address="Restaurant Address Here", # We can refine this later
            dropoff_address=instance.delivery_address,
            delivery_fee=instance.payout_amount,
            status='pending'
        )