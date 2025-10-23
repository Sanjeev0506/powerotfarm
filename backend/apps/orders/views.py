import json
from decimal import Decimal
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
    except Exception:
        return HttpResponseBadRequest('Invalid JSON')

    items = data.get('items') or []
    customer = data.get('customer') or {}

    if not items:
        return JsonResponse({'error': 'No items provided'}, status=400)

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
        # accept either product id or product_name/unit_price
        product_id = it.get('product')
        product_name = it.get('product_name') or it.get('name')
        quantity = int(it.get('quantity', 1))
        unit_price = Decimal(str(it.get('unit_price', '0.00')))

        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                product_name = product.name
                unit_price = product.unit_price
            except Product.DoesNotExist:
                product = None

        item = OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product_name or 'Item',
            quantity=quantity,
            unit_price=unit_price,
        )
        total += unit_price * quantity

    order.total_amount = total
    order.save()

    return JsonResponse({'id': order.id, 'total_amount': str(order.total_amount)})


@csrf_exempt
@require_POST
def pay_order(request, order_id):
    # For now, simulate payment. Later integrate Hubtel.
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

    # Accept optional payload
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = {}

    payment_method = data.get('payment_method', 'cash_on_delivery')

    # If payment_method is hubtel, we would create a payment request here.
    if payment_method == 'cash_on_delivery':
        order.paid = False
        order.save()
        return JsonResponse({'status': 'pending', 'message': 'Cash on delivery selected', 'order_id': order.id})

    # Simulate instant success for demo
    order.paid = True
    order.save()
    return JsonResponse({'status': 'paid', 'order_id': order.id})


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
    order.total_amount = agg.get('total') or Decimal('0.00')
    order.save()

    return JsonResponse({'ok': True, 'order_id': order.id})
