from django.core.management.base import BaseCommand
from apps.core.models import Destination

class Command(BaseCommand):
    help = 'Resets destination views with realistic distribution totaling 2000.'

    def handle(self, *args, **kwargs):
        # Realistic view distribution based on popularity (total = 2000)
        views_data = {
            # HERO / MOST POPULAR (Higher views)
            "Pantai Senggigi": 185,           # #1 Most iconic
            "Gili Nanggu": 142,               # #2 Famous island
            "Taman Narmada": 128,             # #3 Historic heritage
            "Pura Lingsar": 115,              # #4 Famous temple
            "Pura Batu Bolong": 102,          # #5 Sunset spot
            "Hutan Wisata Sesaot": 95,        # #6 Popular forest
            
            # POPULAR (Medium-high views)
            "Gili Sudak": 78,
            "Gili Kedis": 72,
            "Makam Batulayar": 68,
            "Pantai Kerandangan": 65,
            "Desa Wisata Banyumulek": 62,
            "Gili Gede": 58,
            
            # MODERATE (Medium views)
            "Gili Asahan": 52,
            "Gili Layar": 48,
            "Air Terjun Timponan": 45,
            "Pura Suranadi": 42,
            "Kolam Renang Suranadi": 40,
            "Hutan Pusuk (Monkey Forest)": 38,
            "Pantai Mangsit": 36,
            "Pemandian Aik Nyet": 34,
            
            # EMERGING (Lower-medium views)
            "Desa Wisata Kebon Ayu": 32,
            "Ekowisata Mangrove Lembar": 30,
            "Pasar Seni Sesela": 28,
            "Masjid Kuno Wetu Telu Karang Bayan": 26,
            "Pantai Mekaki": 25,
            "Bunut Ngengkang": 24,
            
            # HIDDEN GEMS (Lower views - remote/new)
            "Bangko-Bangko (Desert Point)": 22,
            "Air Terjun Segenter": 20,
            "Desa Wisata Mekarsari": 18,
            "Air Terjun Kekait (Tibu Ijo)": 17,
            "Pantai Nambung": 16,
            "Pantai Elak-Elak": 15,
            "Cafless Waterpark": 14,
            "Gunung Sasak": 13,
            "Makam Keramat Lembar": 12,
            "Pantai Cemare": 11,
        }
        
        updated = 0
        total = 0
        
        for name, views in views_data.items():
            try:
                dest = Destination.objects.get(name=name)
                dest.view_count = views
                dest.save()
                total += views
                self.stdout.write(f"{name}: {views} views")
                updated += 1
            except Destination.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Not found: {name}"))
        
        self.stdout.write(self.style.SUCCESS(f'\n=== DONE ==='))
        self.stdout.write(self.style.SUCCESS(f'Updated: {updated} destinations'))
        self.stdout.write(self.style.SUCCESS(f'Total Views: {total}'))
