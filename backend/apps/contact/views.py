from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


@csrf_exempt
@require_POST
def submit_contact(request):
    # Accept form-encoded or JSON payloads
    data = None
    # try JSON body first
    try:
        import json
        if request.body:
            data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = None

    # fall back to POST form data if JSON not provided
    if not data:
        data = request.POST.dict() if hasattr(request, 'POST') else {}

    form = ContactForm(data)
    if form.is_valid():
        contact = form.save()
        # send notification email
        subject = f"New contact: {contact.subject or 'No subject'}"
        body = f"Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\n\nMessage:\n{contact.message}"
        try:
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_NOTIFICATION_EMAIL])
        except Exception:
            # don't break on email errors; log in real app
            pass
        return JsonResponse({'ok': True, 'id': contact.id})
    else:
        return JsonResponse({'ok': False, 'errors': form.errors}, status=400)


def list_services(request):
    # Placeholder service list - this can be replaced by a proper model later
    services = [
        {
            'id': 1,
            'name': 'Catfish Sale',
            'description': 'Fresh catfish available in various sizes and packaging for both retail and wholesale customers.',
            'prices': [
                {'product_name': 'Hearty Catfish (1kg)', 'unit_price': '25.00'},
                {'product_name': 'Hearty Catfish (5kg)', 'unit_price': '115.00'},
            ]
        },
        {
            'id': 2,
            'name': 'Tilapia Sale',
            'description': 'Premium tilapia, sustainably farmed for superior taste and texture.',
            'prices': [
                {'product_name': 'Premium Tilapia (1kg)', 'unit_price': '30.00'},
                {'product_name': 'Premium Tilapia (5kg)', 'unit_price': '140.00'},
            ]
        },
        {
            'id': 3,
            'name': 'Tarpaulin Pond Sale',
            'description': 'Durable tarpaulin tanks, easy to set up and ideal for small to medium farms.',
            'prices': [
                {'product_name': '5x5x3 feet', 'holding_capacity': '200 fish', 'unit_price': '2000.00'},
                {'product_name': '10x10x3 feet', 'holding_capacity': '1000 fish', 'unit_price': '3500.00'},
            ]
        },
        {
            'id': 4,
            'name': 'Fingerlings Sale',
            'description': 'Healthy fingerlings bred for rapid growth and disease resistance.',
            'prices': [
                {'product_name': 'Catfish Fingerlings (100 pcs)', 'unit_price': '150.00'},
                {'product_name': 'Tilapia Fingerlings (100 pcs)', 'unit_price': '120.00'},
            ]
        },
        {
            'id': 5,
            'name': 'Fish Feed Sale',
            'description': 'High-protein, organic feed formulated to promote excellent growth rates.',
            'prices': [
                {'product_name': '50kg Bag', 'unit_price': '180.00'},
                {'product_name': '25kg Bag', 'unit_price': '95.00'},
            ]
        },
        {
            'id': 6,
            'name': 'Fish Farm Training',
            'description': 'Hands-on training covering pond setup, feeding, health management, and harvesting.',
            'prices': []
        },
        {
            'id': 7,
            'name': 'Consultation',
            'description': 'Expert consultation to optimize your farm for productivity and profitability.',
            'prices': []
        },
    ]
    return JsonResponse(services, safe=False)


def list_gallery(request):
    # Full gallery matching frontend assets so the API-driven gallery shows the same items
    gallery = [
        {'title': 'Feeding Time', 'media_type': 'image'},
        {'title': 'Harvesting the Catch', 'media_type': 'image'},
        {'title': 'Team Collaboration', 'media_type': 'image'},
        {'title': 'Our Pristine Farm', 'media_type': 'video'},
        {'title': 'Netting Session', 'media_type': 'image'},
        {'title': 'Harvesting Environment', 'media_type': 'image'},
        {'title': 'Eel Immersion', 'media_type': 'image'},
        {'title': 'Tarpaulin Tanks', 'media_type': 'image'},
        {'title': 'Fish Feed', 'media_type': 'image'},
        {'title': 'Setting up a Tarpaulin Tank', 'media_type': 'video'},
        {'title': 'Hatchery', 'media_type': 'video'},
        {'title': 'Catfish Fingerlings', 'media_type': 'video'},
        {'title': 'Tilapia Fingerlings', 'media_type': 'video'},
    ]
    return JsonResponse(gallery, safe=False)


def list_process(request):
    process = [
        {
            'step_number': 1,
            'title': 'Eco-Friendly Hatchery',
            'description': 'Our process begins in a state-of-the-art hatchery where we ensure the highest survival rates and genetic quality, without the use of harmful chemicals.',
            'icon_name': 'sprout',
            'image': 'assets/eco-frndly-hatchery.jpg'
        },
        {
            'step_number': 2,
            'title': 'Pure Water Source',
            'description': 'Our fish are raised in pristine, earthen ponds fed by natural water sources. We continuously monitor water quality to mimic their natural habitat.',
            'icon_name': 'droplets',
            'image': 'assets/pure-water-source.jpg'
        },
        {
            'step_number': 3,
            'title': 'Organic Nutrition',
            'description': 'We are committed to providing our fish with high-protein, organic feed, ensuring they are healthy, nutritious, and free from antibiotics.',
            'icon_name': 'leafy-green',
            'image': 'assets/organic-nutrition.png'
        },
        {
            'step_number': 4,
            'title': 'Ethical Harvesting',
            'description': 'We use humane harvesting techniques to minimize stress on the fish, which preserves the quality, texture, and flavor of the final product.',
            'icon_name': 'ship-wheel',
            'image': 'assets/ethical-harvesting.png'
        },
    ]
    return JsonResponse(process, safe=False)
