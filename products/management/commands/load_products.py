import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product, Category


class Command(BaseCommand):
    help = 'products.json se saare products database mein load karo'

    def handle(self, *args, **kwargs):
        json_path = os.path.join(settings.BASE_DIR, 'products.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'products.json nahi mila: {json_path}'))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)

        created_count = 0
        skipped_count = 0

        for item in products_data:
            category, _ = Category.objects.get_or_create(name=item['category'])

            if Product.objects.filter(title=item['title']).exists():
                self.stdout.write(f'  Skip (already exists): {item["title"]}')
                skipped_count += 1
                continue

            Product.objects.create(
                title=item['title'],
                price=item['price'],
                description=item['description'],
                category=category,
            )
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'  Added: {item["title"]} ({item["category"]})'))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Done! {created_count} products add hue, {skipped_count} skip hue.'
        ))
        self.stdout.write(
            'Ab admin se har product ki image upload karo: http://127.0.0.1:8000/admin'
        )
