from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, CustomerProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerSignupForm(UserCreationForm):
    # Address field for the profile
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=True,
    )
    # Adding phone number field to the form
    phone_number = forms.CharField(max_length=15, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        # REMOVED 'password' and ensured all fields match your HTML calls
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, '')
            })
            # Clears labels/help_text for your clean UI look
            field.label = ""
            field.help_text = ""

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        if commit:
            user.save()
            address_data = self.cleaned_data.get('address')
            # Saves the address to the profile
            CustomerProfile.objects.update_or_create(
                user=user, 
                defaults={'address': address_data}
            )
        return user