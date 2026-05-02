from django.db import models
from django.utils.text import slugify

class Restaurant(models.Model):
    # Basic Information
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(help_text="A short bio about the restaurant's cuisine.")
    
    # Visuals & Branding
    # Using your preferred 'images/' or 'restaurants/' path
    logo = models.ImageField(upload_to='restaurant_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='restaurant_covers/', blank=True, null=True)
    
    # Location & Contact (Crucial for the Driver's dashboard)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    # Operations
    is_active = models.BooleanField(default=True, help_text="Is the restaurant currently open for orders?")
    estimated_delivery_time = models.IntegerField(default=30, help_text="Average time in minutes")
    
    # Meta Data
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name