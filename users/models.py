from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Base User model for entire platform.
    Everything indented below belongs to this User.
    """
    
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "admin"
        DRIVER = "DRIVER", "driver"
        CUSTOMER = "CUSTOMER", "customer"
        RESTAURANT = "RESTAURANT", "restaurant"

    # These are now correctly INSIDE the User class
    role = models.CharField(
        max_length=20, 
        choices=Role.choices, 
        default=Role.CUSTOMER
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


# --- CUSTOMER SECTION (Outside User class) ---

class CustomerManager(models.Manager):
    """Manager to return only users with the Customer role."""
    def get_queryset(self, *args, **kwargs):
        # We use User.Role.CUSTOMER to access the choices inside User
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.CUSTOMER)

class Customer(User):
    """
    Proxy Model for Customer logic. 
    """
    objects = CustomerManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.CUSTOMER
        return super().save(*args, **kwargs)


class CustomerProfile(models.Model):
    """
    Stores specific data for Customers, like the delivery address.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"
    
class RestaurantVendorManager(models.Manager):
    """Manager to return only user with restaurant vendor role."""
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.RESTAURANT)
    
class RestaurantVendor(User):
    """Proxy model for Restaurant vendor users."""
    objects = RestaurantVendorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = User.Role.RESTAURANT
        return super().save(*args, **kwargs)