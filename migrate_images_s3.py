import boto3
from django.conf import settings
from products.models import Product

def migrate_images_to_s3():
    if settings.DEBUG:
        print("This script is intended for production only (DEBUG=FALSE).")
        return
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    products = Product.objects.filter(image__isnull=False)

    for product in products:
        image_field = product.image
        s3_key = f"media/{image_field.name}"

        try:
            with image_field.open('rb') as image_file:
                s3_client.upload_fileobj(
                    image_file,
                    settings.AWS_STORAGE_BUCKET_NAME,
                    s3_key,
                    ExtraArgs={'ACL': 'public-read'}
    
                )
            print(f'uploaded {image_field.name} to s3')
        except Exception as e:
            print(f"Error uploading {image_field.name}: {e}")