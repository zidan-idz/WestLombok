from django.core.management.base import BaseCommand
from apps.core.models import Destinasi
import random

class Command(BaseCommand):
    help = 'Populates info_tambahan field with dummy data'

    def handle(self, *args, **kwargs):
        destinations = Destinasi.objects.all()
        
        infos = [
            "Harga Tiket: Rp 5.000\nJam Buka: 08:00 - 17:00 WITA\nFasilitas: Parkir, Toilet, Musholla",
            "Harga Tiket: Gratis\nJam Buka: 24 Jam\nFasilitas: Area Duduk, Spot Foto",
            "Harga Tiket: Rp 10.000\nJam Buka: 07:00 - 18:00 WITA\nFasilitas: Warung Makan, Sewa Perahu",
            "Harga Tiket: Rp 15.000\nJam Buka: 09:00 - 17:00 WITA\nFasilitas: Pemandu Lokal, Toilet Bersih",
            "Harga Tiket: Rp 2.000 (Parkir)\nJam Buka: 06:00 - 18:00 WITA\nFasilitas: Spot Sunset terbaik"
        ]

        count = 0
        for dest in destinations:
            info = random.choice(infos)
            dest.info_tambahan = info
            dest.save()
            count += 1
            self.stdout.write(f'Updated {dest.nama_destinasi}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} destinations with dummy info_tambahan'))
