from django.core.management.base import BaseCommand
from apps.core.models import Kategori, Destinasi
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cleaning old data...')
        Destinasi.objects.all().delete()
        Kategori.objects.all().delete()

        # Ensure a user exists
        user = User.objects.first()
        if not user:
            user = User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write('Created superuser: admin')

        self.stdout.write('Creating Categories...')
        categories_data = [
            {'name': 'Exotic Beaches', 'icon': 'beach_access', 'desc': 'Relax on the most beautiful sandy shores.'},
            {'name': 'Majestic Mountains', 'icon': 'landscape', 'desc': 'Hiking trails and breathtaking peaks.'},
            {'name': 'Cultural Heritage', 'icon': 'temple_buddhist', 'desc': 'Explore ancient temples and local traditions.'},
            {'name': 'Culinary Delights', 'icon': 'restaurant', 'desc': 'Taste the best local and international cuisines.'},
        ]

        categories = {}
        for cat in categories_data:
            c = Kategori.objects.create(
                nama_kategori=cat['name'],
                deskripsi=cat['desc'],
                icon=cat['icon']
            )
            categories[cat['name']] = c
            self.stdout.write(f"Created Category: {cat['name']}")

        self.stdout.write('Creating Destinations...')
        
        # List of available images in media/destinations/primary
        images = [
            'destinations/primary/Kampung-Dzi-Ain-700x394.jpg',
            'destinations/primary/images (1).jpg',
            'destinations/primary/images (2).jpg',
            'destinations/primary/images (3).jpg',
            'destinations/primary/images (4).jpg',
            'destinations/primary/images (5).jpg',
            'destinations/primary/images.jpg',
            'destinations/primary/piaynemo-dan-telaga-bintang-raja-ampat-5_169.jpeg',
            'destinations/primary/shutterstock_132953783.webp',
            'destinations/primary/tempat-wisata-di-brazil.jpg',
            'destinations/primary/tempat-wisata-di-jawa-tengah.webp',
            'destinations/primary/unnamed (1).jpg',
            'destinations/primary/unnamed.jpg',
            'destinations/primary/wisata-bali.jpg',
            'destinations/primary/wisata_di_Indonesia.jpg',
        ]

        # 15 Dummy Destinations
        destinations_data = [
            {
                'name': 'Raja Ampat Islands',
                'cat': 'Exotic Beaches',
                'desc': 'Raja Ampat is a majestic archipelago in Indonesia, famous for its coral reefs and marine life. It is a diver\'s paradise offering crystal clear waters and stunning views.',
                'kec': 'Sekotong', # Valid choice from models
                'img': 'destinations/primary/piaynemo-dan-telaga-bintang-raja-ampat-5_169.jpeg'
            },
            {
                'name': 'Borobudur Temple',
                'cat': 'Cultural Heritage',
                'desc': 'Borobudur is the largest Buddhist temple in the world. Built in the 9th century, it is a UNESCO World Heritage site and a masterpiece of Buddhist architecture.',
                'kec': 'Lembar',
                'img': 'destinations/primary/tempat-wisata-di-jawa-tengah.webp'
            },
            {
                'name': 'Copacabana Beach',
                'cat': 'Exotic Beaches',
                'desc': 'Copacabana is one of the most famous beaches in the world, located in Rio de Janeiro. It stretches for 4 km and is vibrant with life, music, and sports.',
                'kec': 'Batu Layar',
                'img': 'destinations/primary/tempat-wisata-di-brazil.jpg'
            },
            {
                'name': 'Mount Fuji',
                'cat': 'Majestic Mountains',
                'desc': 'Mount Fuji is an active volcano and the highest peak in Japan. It is considered one of Japan\'s three sacred mountains and has been a place of pilgrimage for centuries.',
                'kec': 'Gunung Sari',
                'img': 'destinations/primary/images (2).jpg'
            },
            {
                'name': 'Grand Canyon',
                'cat': 'Majestic Mountains',
                'desc': 'The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona. It is known for its visually overwhelming size and its intricate and colorful landscape.',
                'kec': 'Lingsar',
                'img': 'destinations/primary/images.jpg'
            },
            {
                'name': 'Traditional Village',
                'cat': 'Cultural Heritage',
                'desc': 'Experience the simple and authentic life of the locals in this traditional village. Learn about their customs, crafts, and daily routines.',
                'kec': 'Narmada',
                'img': 'destinations/primary/Kampung-Dzi-Ain-700x394.jpg'
            },
            {
                'name': 'Senggigi Beach',
                'cat': 'Exotic Beaches',
                'desc': 'Senggigi is the main tourist strip of the Indonesian island of Lombok. It offers beautiful sunsets, white sandy beaches, and a relaxed atmosphere.',
                'kec': 'Batu Layar',
                'img': 'destinations/primary/wisata-bali.jpg' # Using bali img as placeholder
            },
            {
                'name': 'Spicy Lombok Chicken',
                'cat': 'Culinary Delights',
                'desc': 'Ayam Taliwang is a spicy grilled chicken dish from Lombok. It is known for its extreme spiciness and rich flavor, usually served with Plecing Kangkung.',
                'kec': 'Mataram', # Not in list but fine, or assign existing
                'img': 'destinations/primary/images (3).jpg'
            },
            {
                'name': 'Hidden Waterfall',
                'cat': 'Majestic Mountains',
                'desc': 'Discover a secluded waterfall deep in the jungle. A perfect spot for nature lovers seeking tranquility and fresh air.',
                'kec': 'Lingsar',
                'img': 'destinations/primary/unnamed.jpg'
            },
            {
                'name': 'Historic Old Town',
                'cat': 'Cultural Heritage',
                'desc': 'Walk through the cobblestone streets of the Old Town, where colonial architecture meets local history. Great for photography and cultural immersion.',
                'kec': 'Lembar',
                'img': 'destinations/primary/images (4).jpg'
            },
            {
                'name': 'Tropical Paradise',
                'cat': 'Exotic Beaches',
                'desc': 'An untouched tropical island with palm trees and turquoise water. Ideal for honeymooners or anyone wanting to escape the city.',
                'kec': 'Sekotong',
                'img': 'destinations/primary/images (5).jpg'
            },
            {
                'name': 'Street Food Market',
                'cat': 'Culinary Delights',
                'desc': 'Explore the bustling night market offering a variety of local street food. From satay to sweet pancakes, satisfy your cravings here.',
                'kec': 'Gerung',
                'img': 'destinations/primary/unnamed (1).jpg'
            },
            {
                'name': 'Ancient Ruins',
                'cat': 'Cultural Heritage',
                'desc': 'Visit the ancient ruins of a lost civilization. These archaeological sites provide a glimpse into the past and are surrounded by mystery.',
                'kec': 'Labuapi',
                'img': 'destinations/primary/shutterstock_132953783.webp'
            },
             {
                'name': 'Blue Lagoon',
                'cat': 'Exotic Beaches',
                'desc': 'The Blue Lagoon is famous for its stunning blue water and white sand. It is a popular spot for snorkeling and swimming.',
                'kec': 'Sekotong',
                'img': 'destinations/primary/images (1).jpg'
            },
             {
                'name': 'Mountain Retreat',
                'cat': 'Majestic Mountains',
                'desc': 'A cozy retreat located high in the mountains. Enjoy cool weather, panoramic views, and warm hospitality.',
                'kec': 'Gunung Sari',
                'img': 'destinations/primary/wisata_di_Indonesia.jpg'
            },

        ]

        count = 0
        for data in destinations_data:
            Destinasi.objects.create(
                nama_destinasi=data['name'],
                deskripsi=data['desc'],
                kategori=categories[data['cat']],
                kecamatan=data.get('kec', 'Batu Layar'),
                lokasi_maps='https://maps.google.com',
                foto_utama=data['img'],
                pengelola=user
            )
            count += 1
            self.stdout.write(f"Created Destinasi: {data['name']}")

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} Destinations and 4 Categories!'))
