# Unit tests untuk aplikasi core
# Tests mencakup:
# - Model Category: validasi, slug, format ikon
# - Model Destination: validasi, slug, relasi
# - Views: List views, Detail views, kode respons
# - URL routing: memastikan semua pola URL berfungsi

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Destination, District
import tempfile
from PIL import Image
import io


class CategoryModelTest(TestCase):
    # Test cases untuk model Category.
    
    def setUp(self):
        # Setup data untuk setiap test.
        self.category = Category.objects.create(
            name="Beach",
            description="Beautiful beach destinations",
            icon="beach_access"
        )
    
    def test_category_creation(self):
        # Test pembuatan kategori berhasil.
        self.assertEqual(self.category.name, "Beach")
        self.assertEqual(self.category.description, "Beautiful beach destinations")
        self.assertIsNotNone(self.category.pk)
    
    def test_category_str_representation(self):
        # Test representasi string model.
        self.assertEqual(str(self.category), "Beach")
    
    def test_slug_auto_generated(self):
        # Test slug dibuat otomatis dari nama kategori.
        self.assertEqual(self.category.slug, "beach")
    
    def test_slug_unique_on_duplicate_name(self):
        # Test slug unik saat ada nama duplikat.
        category2 = Category.objects.create(
            name="Beach",
            description="Another beach category"
        )
        # Second slug should be different
        self.assertNotEqual(self.category.slug, category2.slug)
        self.assertTrue(category2.slug.startswith("beach-"))
    
    def test_icon_format_lowercase(self):
        # Test icon diformat jadi huruf kecil dengan underscore.
        category = Category.objects.create(
            name="Test Icon",
            icon="Beach Access"
        )
        self.assertEqual(category.icon, "beach_access")
    
    def test_icon_format_hyphen_to_underscore(self):
        # Test tanda hubung di icon diubah jadi underscore.
        category = Category.objects.create(
            name="Test Hyphen",
            icon="beach-access"
        )
        self.assertEqual(category.icon, "beach_access")


class DestinationModelTest(TestCase):
    # Test cases untuk model Destination.
    
    @classmethod
    def setUpTestData(cls):
        # Setup data yang digunakan di semua method test.
        # Create category for relationship
        cls.category = Category.objects.create(
            name="Beach",
            icon="waves"
        )
        cls.district = District.objects.create(name="Batu Layar")
        # Create user for manager
        cls.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
    
    def create_test_image(self):
        # Helper untuk membuat image test.
        # Create simple image for testing
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            name='test_image.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
    
    def test_destination_creation(self):
        # Test pembuatan destinasi berhasil.
        destination = Destination.objects.create(
            name="Senggigi Beach",
            description="The most beautiful beach in West Lombok",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            category=self.category,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.name, "Senggigi Beach")
        self.assertEqual(destination.district, self.district)
        self.assertIsNotNone(destination.pk)
    
    def test_destination_str_representation(self):
        # Test representasi string model.
        destination = Destination.objects.create(
            name="Gili Nanggu",
            description="A beautiful small island",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(str(destination), "Gili Nanggu")
    
    def test_slug_auto_generated(self):
        # Test slug dibuat otomatis dari nama destinasi.
        destination = Destination.objects.create(
            name="Narmada Park",
            description="Historical park",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.slug, "narmada-park")
    
    def test_slug_unique_on_duplicate(self):
        # Test slug unik saat ada nama duplikat.
        destination1 = Destination.objects.create(
            name="Beautiful Beach",
            description="Description 1",
            district=self.district,
            maps_embed_url="https://maps.google.com/test1",
            main_image=self.create_test_image()
        )
        destination2 = Destination.objects.create(
            name="Beautiful Beach",
            description="Description 2",
            district=self.district,
            maps_embed_url="https://maps.google.com/test2",
            main_image=self.create_test_image()
        )
        self.assertNotEqual(destination1.slug, destination2.slug)
    
    def test_category_relationship(self):
        # Test relasi ke kategori berfungsi.
        destination = Destination.objects.create(
            name="Test Relationship",
            description="Test description",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            category=self.category,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.category.name, "Beach")
        self.assertIn(destination, self.category.destinations.all())
    
    def test_manager_relationship(self):
        # Test relasi ke user (manager) berfungsi.
        destination = Destination.objects.create(
            name="Test Manager",
            description="Test description",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            manager=self.user,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.manager.username, "admin")
    
    def test_view_count_default_zero(self):
        # Test default view_count adalah 0.
        destination = Destination.objects.create(
            name="Test Views",
            description="Test description",
            district=self.district,
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.view_count, 0)
    
    # test_district_choices removed as District is now a dynamic model, not a fixed choice field.


class DestinationViewTest(TestCase):
    # Test cases untuk views Destination.
    
    @classmethod
    def setUpTestData(cls):
        # Setup data untuk semua test.
        cls.category = Category.objects.create(
            name="Mountain",
            icon="landscape"
        )
        cls.district = District.objects.create(name="Kuripan")
        # Create test image
        image = Image.new('RGB', (100, 100), color='green')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        cls.test_image = SimpleUploadedFile(
            name='test.jpg',
            content=image_io.read(),
            content_type='image/jpeg'
        )
        
        cls.destination = Destination.objects.create(
            name="Sasak Mountain",
            description="Mountain with beautiful view",
            district=cls.district,
            maps_embed_url="https://maps.google.com/test",
            category=cls.category,
            main_image=cls.test_image
        )
    
    def setUp(self):
        # Setup client untuk setiap test.
        self.client = Client()
    
    def test_destination_list_view_status_code(self):
        # Test view list destinasi mengembalikan 200.
        response = self.client.get(reverse('core:destination_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_destination_list_view_template(self):
        # Test list destinasi menggunakan template yang benar.
        response = self.client.get(reverse('core:destination_list'))
        self.assertTemplateUsed(response, 'core/destination_list.html')
    
    def test_destination_list_view_context(self):
        # Test list destinasi memiliki context yang benar.
        response = self.client.get(reverse('core:destination_list'))
        self.assertIn('destination_list', response.context)
        self.assertIn('category_list', response.context)
    
    def test_destination_detail_view_status_code(self):
        # Test view detail destinasi mengembalikan 200.
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_destination_detail_view_template(self):
        # Test detail destinasi menggunakan template yang benar.
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.assertTemplateUsed(response, 'core/destination_detail.html')
    
    def test_destination_detail_increments_views(self):
        # Test counter view bertambah saat halaman dikunjungi.
        initial_views = self.destination.view_count
        self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.destination.refresh_from_db()
        self.assertEqual(self.destination.view_count, initial_views + 1)
    
    def test_destination_detail_404_for_invalid_slug(self):
        # Test 404 untuk slug yang tidak ada.
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': 'does-not-exist'})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_destination_search_filter(self):
        # Test fitur pencarian destinasi.
        response = self.client.get(
            reverse('core:destination_list'),
            {'q': 'Sasak'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sasak Mountain')
    
    def test_destination_category_filter(self):
        # Test filter berdasarkan kategori.
        response = self.client.get(
            reverse('core:destination_list'),
            {'category': self.category.slug}
        )
        self.assertEqual(response.status_code, 200)


class CategoryViewTest(TestCase):
    # Test cases untuk views Category.
    
    @classmethod
    def setUpTestData(cls):
        # Setup data untuk semua test.
        cls.category = Category.objects.create(
            name="Culture",
            description="Cultural and historical tourism",
            icon="temple_hindu"
        )
    
    def setUp(self):
        # Setup client untuk setiap test.
        self.client = Client()
    
    def test_category_list_view_status_code(self):
        # Test view list kategori mengembalikan 200.
        response = self.client.get(reverse('core:category_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_view_template(self):
        # Test list kategori menggunakan template yang benar.
        response = self.client.get(reverse('core:category_list'))
        self.assertTemplateUsed(response, 'core/category_list.html')
    
    def test_category_detail_view_status_code(self):
        # Test view detail kategori mengembalikan 200.
        response = self.client.get(
            reverse('core:category_detail', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_category_detail_view_template(self):
        # Test detail kategori menggunakan template yang benar.
        response = self.client.get(
            reverse('core:category_detail', kwargs={'slug': self.category.slug})
        )
        self.assertTemplateUsed(response, 'core/category_detail.html')


class BaseViewTest(TestCase):
    # Test cases untuk views di apps.base.
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_home_view_status_code(self):
        # Test view home mengembalikan 200.
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        # Test home menggunakan template yang benar.
        response = self.client.get(reverse('base:home'))
        self.assertTemplateUsed(response, 'base/home.html')
    
    def test_about_view_status_code(self):
        # Test view about mengembalikan 200.
        response = self.client.get(reverse('base:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        # Test about menggunakan template yang benar.
        response = self.client.get(reverse('base:about'))
        self.assertTemplateUsed(response, 'base/about.html')


class SurpriseMeViewTest(TestCase):
    # Test cases untuk fitur Surprise Me.
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_surprise_view_status_code(self):
        # Test view surprise mengembalikan 200.
        response = self.client.get(reverse('core:surprise_me'))
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_view_template(self):
        # Test surprise menggunakan template yang benar.
        response = self.client.get(reverse('core:surprise_me'))
        self.assertTemplateUsed(response, 'core/surprise.html')
    
    def test_surprise_view_context(self):
        # Test view surprise memiliki destination_list di context.
        response = self.client.get(reverse('core:surprise_me'))
        self.assertIn('destination_list', response.context)


class URLRoutingTest(TestCase):
    # Test URL routing berfungsi dengan benar.
    
    def test_home_url_resolves(self):
        # Test URL home dapat diakses.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_url_resolves(self):
        # Test URL about dapat diakses.
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_destination_list_url_resolves(self):
        # Test URL list destinasi dapat diakses.
        response = self.client.get('/destinations/')
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_url_resolves(self):
        # Test URL list kategori dapat diakses.
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_url_resolves(self):
        # Test URL surprise dapat diakses.
        response = self.client.get('/surprise/')
        self.assertEqual(response.status_code, 200)
