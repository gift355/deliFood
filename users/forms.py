from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerSignupForm(UserCreationForm):
    # Defining address here allows us to force it into a Textarea
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=True,
        label="Delivery Address"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Order matters for the UI
        fields = ['first_name', 'last_name', 'username','password' ,'email', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mapping field names to your UI's specific placeholders
        placeholders = {
            'first_name': 'Enter first name',
            'last_name': 'Enter last name',
            'username': 'Choose a unique username',
            'password1': 'Create a strong password',
            'password2': 'Repeat password',
            'email': 'you@example.com',
            'phone_number': '+234 xxxx xxxx',
            'address': '5, Estate town'
        }

        for field_name, field in self.fields.items():
            # Add Bootstrap class and Placeholder
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, '')
            })
            # Remove labels and help text for that clean Material look
            field.label = ""
            field.help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        if commit:
            user.save()
            address_data = self.cleaned_data.get('address')
            # Saves the address to the profile correctly
            CustomerProfile.objects.update_or_create(
                user=user, 
                defaults={'address': address_data}
            )
        return user