from django.core.management.base import BaseCommand
from django.conf import settings
from main_app.models import Product
import json
from pathlib import Path
from decimal import Decimal


class Command(BaseCommand):
    help = "Load product entries from data.json (only main_app.product objects)."

    def handle(self, *args, **options):
        data_file = Path(settings.BASE_DIR) / 'data.json'
        if not data_file.exists():
            self.stdout.write(self.style.ERROR(f"data.json not found at {data_file}"))
            return

        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to read data.json: {e}"))
            return

        count = 0
        for obj in data:
            if obj.get('model') == 'main_app.product':
                fields = obj.get('fields', {})
                name = fields.get('name')
                description = fields.get('description', '')
                price = fields.get('price', '0')
                image = fields.get('image')

                if not name:
                    continue

                try:
                    price_val = Decimal(str(price))
                except Exception:
                    price_val = Decimal('0')

                product, created = Product.objects.update_or_create(
                    name=name,
                    defaults={
                        'description': description,
                        'price': price_val,
                        'image': image,
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Loaded/updated {count} product(s)."))
