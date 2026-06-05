from django import forms
from .models import Restaurant

class RestaurantOnboardingForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        # We capture everything needed for a complete storefront profile
        fields = ['name', 'description', 'logo', 'cover_image', 'address', 'phone_number', 'email', 'estimated_delivery_time']
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Ultimate Suya & Grills'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your delicious cuisine to hungry customers...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Physical business address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business phone contact'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Business email address'}),
            'estimated_delivery_time': forms.NumberInput(attrs={'class': 'form-control', 'min': 10}),
        }