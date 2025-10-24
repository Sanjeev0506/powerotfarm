from django.core.management.base import BaseCommand
from apps.orders.models import Product


class Command(BaseCommand):
    help = 'Seed initial products'

    def handle(self, *args, **options):
        products = [
            {'name': 'Premium Tilapia', 'slug': 'premium-tilapia', 'description': 'Premium tilapia', 'unit_price': '30.00'},
            {'name': 'Hearty Catfish', 'slug': 'hearty-catfish', 'description': 'Fresh catfish', 'unit_price': '25.00'},
            {'name': 'Tarpaulin Fish Tanks', 'slug': 'tarpaulin-fish-tanks', 'description': 'Tarpaulin tanks', 'unit_price': '1200.00'},
        ]

        for p in products:
            obj, created = Product.objects.get_or_create(slug=p['slug'], defaults=p)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product {obj.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Product {obj.name} already exists"))
