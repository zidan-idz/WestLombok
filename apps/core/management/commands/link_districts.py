from django.core.management.base import BaseCommand
from apps.core.models import Destination, District

class Command(BaseCommand):
    help = 'Link Destinations to their new District objects'

    def handle(self, *args, **options):
        destinations = Destination.objects.all()
        for dest in destinations:
            if dest.district: # Old CharField
                try:
                    district_obj = District.objects.get(name=dest.district.strip())
                    # We can't save to the FK field yet because it's not in the model! 
                    # WAIT. I reverted the model to ONLY have CharField to pass migration.
                    # I need to Add the FK field BACK now.
                    self.stdout.write(f"Found match: {dest.name} -> {district_obj.name}")
                except District.DoesNotExist:
                     self.stdout.write(self.style.ERROR(f"No match for {dest.name}"))
