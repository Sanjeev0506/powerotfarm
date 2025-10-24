import json
import decimal
from decimal import Decimal, ROUND_HALF_UP
from django.http import JsonResponse, HttpResponseBadRequest
from django.db.models import Sum, F
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, OrderItem


def list_products(request):
    # Return a simple JSON list of products
    products = Product.objects.all().values('id', 'name', 'description', 'unit_price')
    return JsonResponse(list(products), safe=False)


@csrf_exempt
@require_POST
def create_order(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print("Received order data:", json.dumps(data, indent=2))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    items = data.get('items') or []
    customer = data.get('customer') or {}

    if not items:
        return JsonResponse({'error': 'No items provided'}, status=400)

    # Validate that each item has quantity and unit_price
    for item in items:
        if 'quantity' not in item or 'unit_price' not in item:
            return JsonResponse({'error': 'Each item must have quantity and unit_price'}, status=400)
        # Ensure values are numeric
        try:
            item['quantity'] = int(item['quantity'])
            item['unit_price'] = Decimal(str(item['unit_price']))
        except (ValueError, TypeError, decimal.InvalidOperation):
            return JsonResponse({'error': 'Invalid quantity or unit_price'}, status=400)

    # Basic customer data
    name = customer.get('name') or data.get('customer_name') or 'Guest'
    email = customer.get('email') or data.get('customer_email') or ''
    phone = customer.get('phone') or data.get('customer_phone') or ''
    address = customer.get('address') or data.get('shipping_address') or ''
    notes = customer.get('notes') or data.get('notes') or ''

    order = Order.objects.create(
        customer_name=name,
        customer_email=email,
        customer_phone=phone,
        shipping_address=address,
        notes=notes,
    )

    total = Decimal('0.00')
    for it in items:
        product_id = it.get('product')
        product_name = it.get('product_name') or it.get('name')
        quantity = int(it['quantity'])  # Already validated
        unit_price = Decimal(str(it['unit_price']))  # Already validated

        # Only use product for reference, NOT for price
        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                if not product_name:
                    product_name = product.name
            except Product.DoesNotExist:
                pass

        print(f"Creating order item: {quantity}x {product_name} @ {unit_price} each")
        
        item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product_name or 'Item',
            quantity=quantity,
            unit_price=unit_price,
        )
        
        item_total = unit_price * quantity
        print(f"Item total for {quantity}x {product_name}: {item_total} (unit price: {unit_price})")
        total += item_total

    print(f"Subtotal before tax: {total}")
    
    # apply tax to match frontend behaviour (5% VAT)
    TAX_RATE = Decimal('0.05')
    tax = (total * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_with_tax = (total + tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    print(f"Tax amount ({TAX_RATE * 100}%): {tax}")
    print(f"Final total with tax: {total_with_tax}")

    order.total_amount = total_with_tax
    order.save()

    return JsonResponse({'id': order.id, 'total_amount': str(order.total_amount)})


@csrf_exempt
@require_POST
def pay_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    # Accept optional payload
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = {}

    # Get customer phone number for payment
    customer_phone = data.get('phone_number') or order.customer_phone
    if not customer_phone:
        return JsonResponse({'error': 'Customer phone number is required'}, status=400)

    # Create Hubtel payment request
    from apps.payments.gateways import create_hubtel_payment
    payment_response = create_hubtel_payment(order, customer_phone)
    
    if payment_response.get('status') == 'error':
        return JsonResponse({
            'status': 'error',
            'message': payment_response.get('message', 'Payment initialization failed')
        }, status=500)

    # Return checkout URL and payment data
    return JsonResponse({
        'status': payment_response.get('status'),
        'checkout_url': payment_response.get('data', {}).get('checkoutUrl'),
        'client_reference': payment_response.get('data', {}).get('clientReference'),
        'order_id': order.id
    })


@csrf_exempt
@require_POST
def fish_sales_order(request):
    """Simple endpoint to accept fish sales order from frontend process page."""
    import json
    from decimal import Decimal

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    # Minimal fields
    name = data.get('customer_name')
    phone = data.get('phone_number')
    avg_weight = data.get('average_weight')
    quantity = data.get('quantity')
    location = data.get('location')

    if not (name and phone and avg_weight and quantity and location):
        return JsonResponse({'error': 'Missing required fields'}, status=400)

    # Create a lightweight Order record with a generic product entry
    order = Order.objects.create(
        customer_name=name,
        customer_email='',
        customer_phone=phone,
        shipping_address=location,
        notes=f'Fish sales order - avg_weight:{avg_weight}',
    )

    # Create a generic OrderItem record for fish sales
    # Use a placeholder Product if available
    product = None
    try:
        product = Product.objects.filter(name__icontains='Catfish').first() or Product.objects.first()
    except Exception:
        product = None

    unit_price = Decimal(str(data.get('unit_price', '0.00')))
    if not unit_price and product:
        unit_price = product.unit_price

    OrderItem.objects.create(
        order=order,
        product=product,
        product_name=product.name if product else 'Fish Sales',
        quantity=int(quantity),
        unit_price=unit_price,
    )

    agg = order.items.aggregate(total=Sum(F('unit_price') * F('quantity')))
    subtotal = agg.get('total') or Decimal('0.00')
    TAX_RATE = Decimal('0.05')
    tax = (subtotal * TAX_RATE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    order.total_amount = (subtotal + tax).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    order.save()

    return JsonResponse({'ok': True, 'order_id': order.id})
