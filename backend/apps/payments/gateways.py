"""
Hubtel payment gateway integration for PowerOT Farms.
"""

import os
import requests
from django.conf import settings
from decimal import Decimal

HUBTEL_INITIATE_URL = "https://payproxyapi.hubtel.com/items/initiate"
HUBTEL_STATUS_URL = "https://api-txnstatus.hubtel.com/transactions/{pos_sales_id}/status"
HUBTEL_RECEIVE_MONEY_URL = (
    "https://rmp.hubtel.com/merchantaccount/merchants/{pos_sales_id}/receive/mobilemoney"
)

# Hubtel response codes and their meanings
HUBTEL_RESPONSE_CODES = {
    "0000": ("Success", "final"),
    "0001": ("Pending - callback expected", "pending"),
    "2001": ("Payment processor error / failed", "failed"),
    "4000": ("Validation error", "failed"),
    "4070": ("Fees configuration error", "failed"),
    "4101": ("Business not fully set up", "failed"),
    "4103": ("Permission denied", "failed"),
}

def create_hubtel_payment(order, customer_phone, description=None):
    """
    Create a new payment request for an order using Hubtel's API.
    
    Args:
        order: Order model instance
        customer_phone: Customer's phone number
        description: Optional payment description
    
    Returns:
        dict: Payment response with checkout URL and status
    """
    if not hasattr(settings, 'HUBTEL_MERCHANT_ACCOUNT') or not hasattr(settings, 'HUBTEL_API_KEY'):
        return {
            'status': 'error',
            'message': 'Hubtel credentials not configured'
        }

    # Format amount as required by Hubtel (should be Decimal)
    amount = Decimal(str(order.total_amount)).quantize(Decimal('0.01'))
    
    # Prepare description
    if not description:
        description = f"Power OT Farms - Order #{order.id}"

    # Build API request
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {settings.HUBTEL_API_KEY}",
        "Cache-Control": "no-cache"
    }

    # Callback URLs (should be configured in settings for production)
    base_url = settings.SITE_URL if hasattr(settings, 'SITE_URL') else 'http://127.0.0.1:8000'
    
    payload = {
        "totalAmount": float(amount),
        "description": description,
        "callbackUrl": f"{base_url}/api/payments/hubtel/callback/",
        "returnUrl": f"{base_url}/payment-success.html",
        "merchantAccountNumber": settings.HUBTEL_MERCHANT_ACCOUNT,
        "cancellationUrl": f"{base_url}/payment-failed.html",
        "clientReference": f"order_{order.id}",
        "payeeName": order.customer_name,
        "payeeMobileNumber": customer_phone,
        "payeeEmail": order.customer_email
    }

    try:
        response = requests.post(
            HUBTEL_INITIATE_URL,
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        result = response.json()
        
        # Normalize response
        normalized = normalize_hubtel_response(result)
        
        if normalized['status'] == 'pending':
            # Store any needed reference numbers for status checks
            # You might want to create a PaymentTransaction model to track this
            pass
            
        return normalized
        
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'Payment request failed: {str(e)}',
            'code': None,
            'data': None
        }

def check_payment_status(order_id, client_reference=None):
    """
    Check payment status for an order.
    
    Args:
        order_id: Order ID to check
        client_reference: Optional client reference from Hubtel
    
    Returns:
        dict: Payment status information
    """
    if not client_reference:
        client_reference = f"order_{order_id}"

    if not hasattr(settings, 'HUBTEL_MERCHANT_ACCOUNT') or not hasattr(settings, 'HUBTEL_API_KEY'):
        return {
            'status': 'error',
            'message': 'Hubtel credentials not configured'
        }

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {settings.HUBTEL_API_KEY}"
    }

    try:
        response = requests.get(
            HUBTEL_STATUS_URL.format(pos_sales_id=settings.HUBTEL_MERCHANT_ACCOUNT),
            headers=headers,
            params={"clientReference": client_reference}
        )
        response.raise_for_status()
        return normalize_hubtel_response(response.json())
        
    except requests.exceptions.RequestException as e:
        return {
            'status': 'error',
            'message': f'Status check failed: {str(e)}',
            'code': None,
            'data': None
        }

def normalize_hubtel_response(resp_json):
    """
    Normalize Hubtel API responses into a consistent format.
    
    Args:
        resp_json: Raw JSON response from Hubtel
    
    Returns:
        dict: Normalized response with consistent keys
    """
    if not isinstance(resp_json, dict):
        return {
            'code': None,
            'status': 'error',
            'message': 'Invalid response format',
            'data': None
        }

    # Handle different response formats
    code = resp_json.get('ResponseCode') or resp_json.get('responseCode')
    message = resp_json.get('Message') or resp_json.get('message', '')
    data = resp_json.get('Data') or resp_json.get('data')

    if code in HUBTEL_RESPONSE_CODES:
        _, mapped_status = HUBTEL_RESPONSE_CODES[code]
        status = mapped_status
    else:
        # Check data.status if available
        status_field = None
        if isinstance(data, dict):
            status_field = data.get('status') or data.get('Status', '').lower()
            if status_field == 'paid':
                status = 'final'
            elif status_field in ('unpaid', 'failed'):
                status = 'failed'
            else:
                status = 'pending'
        else:
            status = 'error'

    return {
        'code': code,
        'status': status,
        'message': message,
        'data': data
    }
