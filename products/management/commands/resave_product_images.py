from django.core.management.base import BaseCommand
from products.models import Product
class Command(BaseCommand):
    help = 'Re-save all product images to trigger re-upload to S3'

    def handle(self, *args, **kwargs):
        updated = 0
        for product in Product.objects.all():
            if product.image:
                image = product.image
                product.image = image
                product.save()
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Updated: {product.name}'))
        self.stdout.write(self.style.SUCCESS(f'Updated {updated} products'))