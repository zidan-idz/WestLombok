"""
Unit tests untuk aplikasi core

Tests mencakup:
- Model Kategori: validasi, slug generation, icon formatting
- Model Destinasi: validasi, slug generation, relasi
- Views: List views, Detail views, response codes
- URL routing: memastikan semua URL patterns bekerja
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Kategori, Destinasi
import tempfile
from PIL import Image
import io


class KategoriModelTest(TestCase):
    """Test cases untuk model Kategori."""
    
    def setUp(self):
        """Setup data untuk setiap test."""
        self.kategori = Kategori.objects.create(
            nama_kategori="Pantai",
            deskripsi="Destinasi pantai yang indah",
            icon="beach_access"
        )
    
    def test_kategori_creation(self):
        """Test pembuatan kategori berhasil."""
        self.assertEqual(self.kategori.nama_kategori, "Pantai")
        self.assertEqual(self.kategori.deskripsi, "Destinasi pantai yang indah")
        self.assertIsNotNone(self.kategori.pk)
    
    def test_kategori_str_representation(self):
        """Test string representation model."""
        self.assertEqual(str(self.kategori), "Pantai")
    
    def test_slug_auto_generated(self):
        """Test slug otomatis dibuat dari nama kategori."""
        self.assertEqual(self.kategori.slug, "pantai")
    
    def test_slug_unique_on_duplicate_name(self):
        """Test slug unik jika ada nama duplikat."""
        kategori2 = Kategori.objects.create(
            nama_kategori="Pantai",
            deskripsi="Kategori pantai lain"
        )
        # Slug kedua harus berbeda
        self.assertNotEqual(self.kategori.slug, kategori2.slug)
        self.assertTrue(kategori2.slug.startswith("pantai-"))
    
    def test_icon_format_lowercase(self):
        """Test icon diformat ke lowercase dengan underscore."""
        kategori = Kategori.objects.create(
            nama_kategori="Test Icon",
            icon="Beach Access"
        )
        self.assertEqual(kategori.icon, "beach_access")
    
    def test_icon_format_hyphen_to_underscore(self):
        """Test hyphen di icon diubah ke underscore."""
        kategori = Kategori.objects.create(
            nama_kategori="Test Hyphen",
            icon="beach-access"
        )
        self.assertEqual(kategori.icon, "beach_access")


class DestinasiModelTest(TestCase):
    """Test cases untuk model Destinasi."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data yang digunakan di semua test methods."""
        # Buat kategori untuk relasi
        cls.kategori = Kategori.objects.create(
            nama_kategori="Pantai",
            icon="waves"
        )
        # Buat user untuk pengelola
        cls.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
    
    def create_test_image(self):
        """Helper untuk membuat test image."""
        # Buat image sederhana untuk testing
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
    
    def test_destinasi_creation(self):
        """Test pembuatan destinasi berhasil."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Pantai Senggigi",
            deskripsi="Pantai terindah di Lombok Barat",
            kecamatan="Batu Layar",
            lokasi_maps="https://maps.google.com/test",
            kategori=self.kategori,
            foto_utama=self.create_test_image()
        )
        self.assertEqual(destinasi.nama_destinasi, "Pantai Senggigi")
        self.assertEqual(destinasi.kecamatan, "Batu Layar")
        self.assertIsNotNone(destinasi.pk)
    
    def test_destinasi_str_representation(self):
        """Test string representation model."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Gili Nanggu",
            deskripsi="Pulau kecil yang cantik",
            kecamatan="Sekotong",
            lokasi_maps="https://maps.google.com/test",
            foto_utama=self.create_test_image()
        )
        self.assertEqual(str(destinasi), "Gili Nanggu")
    
    def test_slug_auto_generated(self):
        """Test slug otomatis dibuat dari nama destinasi."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Taman Narmada",
            deskripsi="Taman bersejarah",
            kecamatan="Narmada",
            lokasi_maps="https://maps.google.com/test",
            foto_utama=self.create_test_image()
        )
        self.assertEqual(destinasi.slug, "taman-narmada")
    
    def test_slug_unique_on_duplicate(self):
        """Test slug unik jika ada nama duplikat."""
        destinasi1 = Destinasi.objects.create(
            nama_destinasi="Pantai Indah",
            deskripsi="Deskripsi 1",
            kecamatan="Sekotong",
            lokasi_maps="https://maps.google.com/test1",
            foto_utama=self.create_test_image()
        )
        destinasi2 = Destinasi.objects.create(
            nama_destinasi="Pantai Indah",
            deskripsi="Deskripsi 2",
            kecamatan="Lembar",
            lokasi_maps="https://maps.google.com/test2",
            foto_utama=self.create_test_image()
        )
        self.assertNotEqual(destinasi1.slug, destinasi2.slug)
    
    def test_kategori_relationship(self):
        """Test relasi ke kategori bekerja."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Test Relasi",
            deskripsi="Test deskripsi",
            kecamatan="Gerung",
            lokasi_maps="https://maps.google.com/test",
            kategori=self.kategori,
            foto_utama=self.create_test_image()
        )
        self.assertEqual(destinasi.kategori.nama_kategori, "Pantai")
        self.assertIn(destinasi, self.kategori.destinasi.all())
    
    def test_pengelola_relationship(self):
        """Test relasi ke user (pengelola) bekerja."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Test Pengelola",
            deskripsi="Test deskripsi",
            kecamatan="Kediri",
            lokasi_maps="https://maps.google.com/test",
            pengelola=self.user,
            foto_utama=self.create_test_image()
        )
        self.assertEqual(destinasi.pengelola.username, "admin")
    
    def test_jumlah_views_default_zero(self):
        """Test jumlah_views default adalah 0."""
        destinasi = Destinasi.objects.create(
            nama_destinasi="Test Views",
            deskripsi="Test deskripsi",
            kecamatan="Lingsar",
            lokasi_maps="https://maps.google.com/test",
            foto_utama=self.create_test_image()
        )
        self.assertEqual(destinasi.jumlah_views, 0)
    
    def test_kecamatan_choices(self):
        """Test kecamatan harus dari pilihan yang valid."""
        valid_kecamatan = [
            'Sekotong', 'Lembar', 'Gerung', 'Labuapi', 'Kediri',
            'Kuripan', 'Narmada', 'Lingsar', 'Gunung Sari', 'Batu Layar'
        ]
        for kec in valid_kecamatan:
            destinasi = Destinasi.objects.create(
                nama_destinasi=f"Test {kec}",
                deskripsi="Test",
                kecamatan=kec,
                lokasi_maps="https://maps.google.com/test",
                foto_utama=self.create_test_image()
            )
            self.assertEqual(destinasi.kecamatan, kec)


class DestinasiViewTest(TestCase):
    """Test cases untuk views Destinasi."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data untuk semua test."""
        cls.kategori = Kategori.objects.create(
            nama_kategori="Gunung",
            icon="landscape"
        )
        # Buat test image
        image = Image.new('RGB', (100, 100), color='green')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        cls.test_image = SimpleUploadedFile(
            name='test.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
        
        cls.destinasi = Destinasi.objects.create(
            nama_destinasi="Gunung Sasak",
            deskripsi="Gunung dengan pemandangan indah",
            kecamatan="Kuripan",
            lokasi_maps="https://maps.google.com/test",
            kategori=cls.kategori,
            foto_utama=cls.test_image
        )
    
    def setUp(self):
        """Setup client untuk setiap test."""
        self.client = Client()
    
    def test_destinasi_list_view_status_code(self):
        """Test destinasi list view returns 200."""
        response = self.client.get(reverse('core:destinasi_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_destinasi_list_view_template(self):
        """Test destinasi list menggunakan template yang benar."""
        response = self.client.get(reverse('core:destinasi_list'))
        self.assertTemplateUsed(response, 'core/destinasi_list.html')
    
    def test_destinasi_list_view_context(self):
        """Test destinasi list memiliki context yang benar."""
        response = self.client.get(reverse('core:destinasi_list'))
        self.assertIn('destinasi_list', response.context)
        self.assertIn('kategori_list', response.context)
    
    def test_destinasi_detail_view_status_code(self):
        """Test destinasi detail view returns 200."""
        response = self.client.get(
            reverse('core:destinasi_detail', kwargs={'slug': self.destinasi.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_destinasi_detail_view_template(self):
        """Test destinasi detail menggunakan template yang benar."""
        response = self.client.get(
            reverse('core:destinasi_detail', kwargs={'slug': self.destinasi.slug})
        )
        self.assertTemplateUsed(response, 'core/destinasi_detail.html')
    
    def test_destinasi_detail_increments_views(self):
        """Test view counter bertambah saat halaman dikunjungi."""
        initial_views = self.destinasi.jumlah_views
        self.client.get(
            reverse('core:destinasi_detail', kwargs={'slug': self.destinasi.slug})
        )
        self.destinasi.refresh_from_db()
        self.assertEqual(self.destinasi.jumlah_views, initial_views + 1)
    
    def test_destinasi_detail_404_for_invalid_slug(self):
        """Test 404 untuk slug yang tidak ada."""
        response = self.client.get(
            reverse('core:destinasi_detail', kwargs={'slug': 'tidak-ada'})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_destinasi_search_filter(self):
        """Test fitur pencarian destinasi."""
        response = self.client.get(
            reverse('core:destinasi_list'),
            {'q': 'Sasak'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Gunung Sasak')
    
    def test_destinasi_kategori_filter(self):
        """Test filter berdasarkan kategori."""
        response = self.client.get(
            reverse('core:destinasi_list'),
            {'kategori': self.kategori.slug}
        )
        self.assertEqual(response.status_code, 200)


class KategoriViewTest(TestCase):
    """Test cases untuk views Kategori."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data untuk semua test."""
        cls.kategori = Kategori.objects.create(
            nama_kategori="Budaya",
            deskripsi="Wisata budaya dan sejarah",
            icon="temple_hindu"
        )
    
    def setUp(self):
        """Setup client untuk setiap test."""
        self.client = Client()
    
    def test_kategori_list_view_status_code(self):
        """Test kategori list view returns 200."""
        response = self.client.get(reverse('core:kategori_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_kategori_list_view_template(self):
        """Test kategori list menggunakan template yang benar."""
        response = self.client.get(reverse('core:kategori_list'))
        self.assertTemplateUsed(response, 'core/kategori_list.html')
    
    def test_kategori_detail_view_status_code(self):
        """Test kategori detail view returns 200."""
        response = self.client.get(
            reverse('core:kategori_detail', kwargs={'slug': self.kategori.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_kategori_detail_view_template(self):
        """Test kategori detail menggunakan template yang benar."""
        response = self.client.get(
            reverse('core:kategori_detail', kwargs={'slug': self.kategori.slug})
        )
        self.assertTemplateUsed(response, 'core/kategori_detail.html')


class BaseViewTest(TestCase):
    """Test cases untuk views di apps.base."""
    
    def setUp(self):
        """Setup client untuk setiap test."""
        self.client = Client()
    
    def test_home_view_status_code(self):
        """Test home view returns 200."""
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Test home menggunakan template yang benar."""
        response = self.client.get(reverse('base:home'))
        self.assertTemplateUsed(response, 'base/home.html')
    
    def test_about_view_status_code(self):
        """Test about view returns 200."""
        response = self.client.get(reverse('base:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        """Test about menggunakan template yang benar."""
        response = self.client.get(reverse('base:about'))
        self.assertTemplateUsed(response, 'base/about.html')


class SurpriseMeViewTest(TestCase):
    """Test cases untuk fitur Surprise Me."""
    
    def setUp(self):
        """Setup client untuk setiap test."""
        self.client = Client()
    
    def test_surprise_view_status_code(self):
        """Test surprise view returns 200."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_view_template(self):
        """Test surprise menggunakan template yang benar."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertTemplateUsed(response, 'core/surprise.html')
    
    def test_surprise_view_context(self):
        """Test surprise view memiliki destinasi_list di context."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertIn('destinasi_list', response.context)


class URLRoutingTest(TestCase):
    """Test URL routing berfungsi dengan benar."""
    
    def test_home_url_resolves(self):
        """Test URL home dapat diakses."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_url_resolves(self):
        """Test URL about dapat diakses."""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_destinasi_list_url_resolves(self):
        """Test URL destinasi list dapat diakses."""
        response = self.client.get('/destinasi/')
        self.assertEqual(response.status_code, 200)
    
    def test_kategori_list_url_resolves(self):
        """Test URL kategori list dapat diakses."""
        response = self.client.get('/kategori/')
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_url_resolves(self):
        """Test URL surprise dapat diakses."""
        response = self.client.get('/surprise/')
        self.assertEqual(response.status_code, 200)
