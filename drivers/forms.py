from django import forms
from .models import DriverProfile

class DriverProfileForm(forms.ModelForm): # Fixed: Removed the underscore
    class Meta:
        model = DriverProfile
        fields = ['vehicle_type', 'license_plate']
        
        # Adding labels makes the UI cleaner for the driver
        labels = {
            'vehicle_type': 'What are you driving?',
            'license_plate': 'Vehicle License Plate Number',
        }
        
        widgets = {
            'vehicle_type': forms.Select(attrs={
                'class': 'form-select p-3 shadow-sm border-0 rounded pill',
                'style': 'background-color: #fdf8ff;'
            }),
            'license_plate': forms.TextInput(attrs={
                'class': 'form-control p-3 shadow-sm border-0 rounded-pill', 
                'placeholder': 'e.g. ABC-123-XY',
                'style': 'background-color: #fdf8ff;'
            }),
        }