from django.core.management.base import BaseCommand
from apps.core.models import Destination, District, DestinationGallery
from django.core.files.base import ContentFile
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Migrate legacy data (District strings & 4 Gallery Images) to new normalized models'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting Data Migration...'))

        destinations = Destination.objects.all()
        
        # 1. Migrate Districts
        for dest in destinations:
            if dest.district: # Field is CharField now
                district_name = dest.district.strip()
                # Create or Get District object
                district_obj, created = District.objects.get_or_create(
                    name=district_name,
                    defaults={'slug': slugify(district_name)}
                )
                if created:
                     self.stdout.write(self.style.SUCCESS(f"Created District: {district_name}"))
            
            # 2. Migrate Images
            self.migrate_images(dest)
        
        self.stdout.write(self.style.SUCCESS('Migration Complete!'))

    def migrate_images(self, dest):
        # List of old fields
        old_fields = ['gallery_image_1', 'gallery_image_2', 'gallery_image_3', 'gallery_image_4']
        
        for field_name in old_fields:
            image_field = getattr(dest, field_name)
            if image_field:
                self.stdout.write(f"Moving {field_name} for {dest.name}")
                # Create detailed Gallery object
                try:
                    DestinationGallery.objects.create(
                        destination=dest,
                        image=image_field 
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to move image: {e}"))
