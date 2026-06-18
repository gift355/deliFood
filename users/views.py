from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .forms import CustomerSignupForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from menu.models import FoodItem
from restaurant.models import Restaurant
from django.contrib.auth.forms import SetPasswordForm
from django.db.models import Q
from .tokens import account_activation_token
# Create your views here.

def landing_view(request):
    return render(request, 'users/landing.html')

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = CustomerSignupForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Lock until email is confirmed
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Activate your DeliFood account"
            
            message = render_to_string("users/activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                # Use your custom token generator here:
                "token": account_activation_token.make_token(user),
            })
            
            user_email = form.cleaned_data.get('email')
            email_msg = EmailMessage(mail_subject, message, to=[user_email])
            
            try:
                email_msg.send()
                messages.success(request, "Account created! Please confirm your email to complete registration.")
            except Exception as e:
                messages.warning(request, f"Account created, but activation email failed to send. Error: {e}")
            
            return redirect("account_activation_notice")
            
    else:
        form = CustomerSignupForm()
        
    return render(request, "users/signup.html", {"form": form})


def account_activation_notice(request):
    return render(request, "users/account_activation_notice.html")

def activate_account(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

     # Using the custom account_activation_token here to validate
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your email has been successfully verified! Welcome to DeliFood.")
        return redirect('login')
    else:
        return render(request, 'users/email_verification_invalid.html')
    

#def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Log in the user immediately after thhey signup
            login(request, user)
            return redirect('home')
    else:
        form = CustomerSignupForm()
    return render(request, 'users/signup.html', {'form': form})


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        try:
            user = User.objects.get(email=email)
            
            # Prepare secure token parameters
            current_site = get_current_site(request)
            subject = "Password Reset Request | DeliFood"
            message = render_to_string("users/password_reset_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                "protocol": "https" if request.is_secure() else "http"
            })
            
            email_msg = EmailMessage(subject, message, to=[email])
            email_msg.send()
            
        except User.DoesNotExist:
            #  We do nothing here! By failing silently, hackers can't phish for real emails.
            pass
        except Exception as e:
            # Catches connection faults with your email backend provider
            messages.error(request, f"System error dispatching recovery sequence: {e}")
            return render(request, "users/password_reset.html")

        #  Always redirect here to trigger your standalone password_reset_done page!
        return redirect("password_reset_done")

    return render(request, "users/password_reset.html")

def password_reset_confirm(request, uidb64, token):
    try:
        # Decode base64 UID back to the user's primary key integer/string
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # Validate that the token matches this specific user and hasn't expired
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been reset successfully.")
                # 🚀 Redirect to your standalone completion template view
                return redirect("password_reset_complete")
        else:
            form = SetPasswordForm(user)
            
        return render(request, "users/password_reset_confirm.html", {"form": form})
    else:
        # Link was manipulated or expired (exceeded PASSWORD_RESET_TIMEOUT)
        messages.error(request, "The password reset link is invalid or has expired.")
        # 🚀 Fixed hyphen to underscore to prevent URL routing crashes
        return redirect("password_reset")
    
def password_reset_done(request):
    return render(request, "users/password_reset_done.html")

def password_reset_complete(request):
    return render(request, "users/password_reset_complete.html")

def login_view(request):
    if request.method == 'POST':
        # 1. Capture the data from the login form
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # 2. Get the validated username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # 3. Check if this user exists in the database (Authentication)
            user = authenticate(username=username, password=password)
            
            if user is not None:
                # 4. Start the session (Login)
                login(request, user)
                return redirect('home') # Go to home page
            else:
                messages.error(request, "Invalid Credentials")
        else:
            messages.error(request, "Invalid Credentials")
    else:
        form = AuthenticationForm()
        
    return render(request, 'users/login.html', {'form': form})

#def home_view(request):
    food_items = FoodItem.objects.filter(available=True).order_by('-id')[:12]
    context = {
        'food_items': food_items,
    }
    return render(request, 'users/home.html', context)
def home_view(request):
    # 1. Capture the search inputs from the GET request
    # 'address' matches the name="" attribute in your delivery address bar
    address_query = request.GET.get('address', '').strip()
    # 'q' can be used for a general food/restaurant name search bar
    food_query = request.GET.get('q', '').strip()

    # 2. Start with all available food items
    food_items = FoodItem.objects.filter(available=True, restaurant__is_active=True)

    # 3. Filter by Location (Address/City)
    # This filters food items based on their restaurant's address
    if address_query:
        food_items = food_items.filter(restaurant__address__icontains=address_query)

    # 4. Filter by Food Name or Restaurant Name
    # This allows a user to search for "Pizza" or "Mama Calabar"
    if food_query:
        food_items = food_items.filter(
            Q(name__icontains=food_query) | 
            Q(restaurant__name__icontains=food_query) |
            Q(description__icontains=food_query)
        )

    # 5. Order and Limit (keeping your original 12-item limit)
    food_items = food_items.order_by('-id')[:12]

    context = {
        'food_items': food_items,
        'address_query': address_query,
        'food_query': food_query,
    }
    return render(request, 'users/home.html', context)


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


