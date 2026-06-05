import os
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from orders.models import Order
from .models import Transaction
from django.urls import reverse


# Create your views here.
@login_required
def initiate_payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, customer=request.user)
    
    # Generate a secure tracking reference code for Paystack
    reference = f"DELI-{order_number}-{get_random_string(5).upper()}"
    
    # Create an audit trail log in our Transaction model
    Transaction.objects.create(
        order=order,
        user=request.user,
        payment_reference=reference,
        payment_gateway='paystack',
        amount=order.total_amount,
        currency='NGN',
        status='initiated'
    )
    
    context = {
        'order': order,
        'paystack_public_key': os.getenv('PAYSTACK_PUBLIC_KEY'),
        'payment_reference': reference,
        'email': request.user.email,
        'amount_in_kobo': int(order.total_amount * 100) # Paystack counts in kobo
    }
    return render(request, 'payments/checkout.html', context)


@login_required
def verify_payment(request, reference):
    transaction = get_object_or_404(Transaction, payment_reference=reference, user=request.user)
    secret_key = os.getenv('PAYSTACK_SECRET_KEY')
    
    # Verify directly with Paystack API servers
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        if response_data.get('status') and response_data['data']['status'] == 'success':
            # 1. Update internal transaction tracking status
            transaction.status = 'successful'
            transaction.gateway_response = response_data
            transaction.save()
            
            # 2. Update order status so restaurant dashboards can see it
            order = transaction.order
            order.status = 'pending' # Shifts from unpaid state to an active order queue
            order.save()
            
            # 3. 🚀 DYNAMIC ROUTE GENERATION:
            # Safely look up the exact 'order_detail' path using the order number
            redirect_url = reverse('orders:order_detail', kwargs={'order_number': order.order_number})
            
            # Pass the URL back inside the JSON response block
            return JsonResponse({
                'status': 'success', 
                'message': 'Payment approved safely.',
                'redirect_url': redirect_url
            })
        else:
            transaction.status = 'failed'
            transaction.gateway_response = response_data
            transaction.save()
            return JsonResponse({'status': 'failed', 'message': 'Payment validation declined.'}, status=400)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

#@login_required
#def verify_payment(request, reference):
    transaction = get_object_or_404(Transaction, payment_reference=reference, user=request.user)
    secret_key = os.getenv('PAYSTACK_SECRET_KEY')
    
    # Verify directly with Paystack API servers
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {secret_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()
        
        if response_data.get('status') and response_data['data']['status'] == 'success':
            # 1. Update internal transaction tracking status
            transaction.status = 'successful'
            transaction.gateway_response = response_data
            transaction.save()
            
            # 2. Update order status so restaurant dashboards can see it
            order = transaction.order
            order.status = 'pending' # Shifts from unpaid state to an active order queue
            order.save()
            
            return JsonResponse({'status': 'success', 'message': 'Payment approved safely.'})
        else:
            transaction.status = 'failed'
            transaction.gateway_response = response_data
            transaction.save()
            return JsonResponse({'status': 'failed', 'message': 'Payment validation declined.'}, status=400)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
