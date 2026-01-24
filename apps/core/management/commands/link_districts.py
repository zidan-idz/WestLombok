from django.core.management.base import BaseCommand
from apps.core.models import Destination, District

class Command(BaseCommand):
    help = 'Populate the new District FK from the district_legacy CharField'

    def handle(self, *args, **options):
        self.stdout.write("Linking Destinations to Districts...")
        
        destinations = Destination.objects.all()
        count = 0
        for dest in destinations:
            if dest.district_legacy:
                try:
                    district_name = dest.district_legacy.strip()
                    district_obj = District.objects.get(name=district_name)
                    dest.district = district_obj
                    dest.save()
                    self.stdout.write(self.style.SUCCESS(f"Linked: {dest.name} -> {district_obj.name}"))
                    count += 1
                except District.DoesNotExist:
                     self.stdout.write(self.style.ERROR(f"No corresponding District found for {dest.name} (Legacy: {dest.district_legacy})"))
        
        self.stdout.write(self.style.SUCCESS(f"Done. Linked {count} destinations."))
