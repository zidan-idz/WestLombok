from django.core.management.base import BaseCommand
from django.core import serializers
from apps.core.models import Destination, Category, District

class Command(BaseCommand):
    help = 'Eksport data Destinasi, Kategori, dan Kecamatan ke file JSON'

    def handle(self, *args, **kwargs):
        self.export_model(Destination, 'Data_Destinasi.json')
        self.export_model(Category, 'Data_Kategori.json')
        self.export_model(District, 'Data_Kecamatan.json')
        self.stdout.write(self.style.SUCCESS('Successfully exported all data to JSON files'))

    def export_model(self, model, filename):
        # Gunakan serializer Django untuk mengubah QuerySet ke JSON
        # indent=4 agar mudah dibaca manusia
        # ensure_ascii=False agar karakter non-ASCII (jika ada) terbaca benar
        data = serializers.serialize("json", model.objects.all(), indent=4, ensure_ascii=False)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)
            
        self.stdout.write(f'Created {filename}')
