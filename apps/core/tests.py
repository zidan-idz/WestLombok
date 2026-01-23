"""
Unit tests for the core application

Tests cover:
- Category model: validation, slug generation, icon formatting
- Destination model: validation, slug generation, relationships
- Views: List views, Detail views, response codes
- URL routing: ensuring all URL patterns work
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Category, Destination
import tempfile
from PIL import Image
import io


class CategoryModelTest(TestCase):
    """Test cases for Category model."""
    
    def setUp(self):
        """Setup data for each test."""
        self.category = Category.objects.create(
            name="Beach",
            description="Beautiful beach destinations",
            icon="beach_access"
        )
    
    def test_category_creation(self):
        """Test category creation is successful."""
        self.assertEqual(self.category.name, "Beach")
        self.assertEqual(self.category.description, "Beautiful beach destinations")
        self.assertIsNotNone(self.category.pk)
    
    def test_category_str_representation(self):
        """Test string representation of model."""
        self.assertEqual(str(self.category), "Beach")
    
    def test_slug_auto_generated(self):
        """Test slug is automatically generated from category name."""
        self.assertEqual(self.category.slug, "beach")
    
    def test_slug_unique_on_duplicate_name(self):
        """Test slug is unique when there are duplicate names."""
        category2 = Category.objects.create(
            name="Beach",
            description="Another beach category"
        )
        # Second slug should be different
        self.assertNotEqual(self.category.slug, category2.slug)
        self.assertTrue(category2.slug.startswith("beach-"))
    
    def test_icon_format_lowercase(self):
        """Test icon is formatted to lowercase with underscore."""
        category = Category.objects.create(
            name="Test Icon",
            icon="Beach Access"
        )
        self.assertEqual(category.icon, "beach_access")
    
    def test_icon_format_hyphen_to_underscore(self):
        """Test hyphen in icon is changed to underscore."""
        category = Category.objects.create(
            name="Test Hyphen",
            icon="beach-access"
        )
        self.assertEqual(category.icon, "beach_access")


class DestinationModelTest(TestCase):
    """Test cases for Destination model."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data used in all test methods."""
        # Create category for relationship
        cls.category = Category.objects.create(
            name="Beach",
            icon="waves"
        )
        # Create user for manager
        cls.user = User.objects.create_user(
            username='admin',
            password='testpass123'
        )
    
    def create_test_image(self):
        """Helper to create test image."""
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
        """Test destination creation is successful."""
        destination = Destination.objects.create(
            name="Senggigi Beach",
            description="The most beautiful beach in West Lombok",
            district="Batu Layar",
            maps_embed_url="https://maps.google.com/test",
            category=self.category,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.name, "Senggigi Beach")
        self.assertEqual(destination.district, "Batu Layar")
        self.assertIsNotNone(destination.pk)
    
    def test_destination_str_representation(self):
        """Test string representation of model."""
        destination = Destination.objects.create(
            name="Gili Nanggu",
            description="A beautiful small island",
            district="Sekotong",
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(str(destination), "Gili Nanggu")
    
    def test_slug_auto_generated(self):
        """Test slug is automatically generated from destination name."""
        destination = Destination.objects.create(
            name="Narmada Park",
            description="Historical park",
            district="Narmada",
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.slug, "narmada-park")
    
    def test_slug_unique_on_duplicate(self):
        """Test slug is unique when there are duplicate names."""
        destination1 = Destination.objects.create(
            name="Beautiful Beach",
            description="Description 1",
            district="Sekotong",
            maps_embed_url="https://maps.google.com/test1",
            main_image=self.create_test_image()
        )
        destination2 = Destination.objects.create(
            name="Beautiful Beach",
            description="Description 2",
            district="Lembar",
            maps_embed_url="https://maps.google.com/test2",
            main_image=self.create_test_image()
        )
        self.assertNotEqual(destination1.slug, destination2.slug)
    
    def test_category_relationship(self):
        """Test relationship to category works."""
        destination = Destination.objects.create(
            name="Test Relationship",
            description="Test description",
            district="Gerung",
            maps_embed_url="https://maps.google.com/test",
            category=self.category,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.category.name, "Beach")
        self.assertIn(destination, self.category.destinations.all())
    
    def test_manager_relationship(self):
        """Test relationship to user (manager) works."""
        destination = Destination.objects.create(
            name="Test Manager",
            description="Test description",
            district="Kediri",
            maps_embed_url="https://maps.google.com/test",
            manager=self.user,
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.manager.username, "admin")
    
    def test_view_count_default_zero(self):
        """Test view_count default is 0."""
        destination = Destination.objects.create(
            name="Test Views",
            description="Test description",
            district="Lingsar",
            maps_embed_url="https://maps.google.com/test",
            main_image=self.create_test_image()
        )
        self.assertEqual(destination.view_count, 0)
    
    def test_district_choices(self):
        """Test district must be from valid choices."""
        valid_districts = [
            'Sekotong', 'Lembar', 'Gerung', 'Labuapi', 'Kediri',
            'Kuripan', 'Narmada', 'Lingsar', 'Gunung Sari', 'Batu Layar'
        ]
        for district in valid_districts:
            destination = Destination.objects.create(
                name=f"Test {district}",
                description="Test",
                district=district,
                maps_embed_url="https://maps.google.com/test",
                main_image=self.create_test_image()
            )
            self.assertEqual(destination.district, district)


class DestinationViewTest(TestCase):
    """Test cases for Destination views."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data for all tests."""
        cls.category = Category.objects.create(
            name="Mountain",
            icon="landscape"
        )
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
            district="Kuripan",
            maps_embed_url="https://maps.google.com/test",
            category=cls.category,
            main_image=cls.test_image
        )
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_destination_list_view_status_code(self):
        """Test destination list view returns 200."""
        response = self.client.get(reverse('core:destination_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_destination_list_view_template(self):
        """Test destination list uses correct template."""
        response = self.client.get(reverse('core:destination_list'))
        self.assertTemplateUsed(response, 'core/destination_list.html')
    
    def test_destination_list_view_context(self):
        """Test destination list has correct context."""
        response = self.client.get(reverse('core:destination_list'))
        self.assertIn('destination_list', response.context)
        self.assertIn('category_list', response.context)
    
    def test_destination_detail_view_status_code(self):
        """Test destination detail view returns 200."""
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_destination_detail_view_template(self):
        """Test destination detail uses correct template."""
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.assertTemplateUsed(response, 'core/destination_detail.html')
    
    def test_destination_detail_increments_views(self):
        """Test view counter increases when page is visited."""
        initial_views = self.destination.view_count
        self.client.get(
            reverse('core:destination_detail', kwargs={'slug': self.destination.slug})
        )
        self.destination.refresh_from_db()
        self.assertEqual(self.destination.view_count, initial_views + 1)
    
    def test_destination_detail_404_for_invalid_slug(self):
        """Test 404 for non-existent slug."""
        response = self.client.get(
            reverse('core:destination_detail', kwargs={'slug': 'does-not-exist'})
        )
        self.assertEqual(response.status_code, 404)
    
    def test_destination_search_filter(self):
        """Test destination search feature."""
        response = self.client.get(
            reverse('core:destination_list'),
            {'q': 'Sasak'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sasak Mountain')
    
    def test_destination_category_filter(self):
        """Test filter by category."""
        response = self.client.get(
            reverse('core:destination_list'),
            {'category': self.category.slug}
        )
        self.assertEqual(response.status_code, 200)


class CategoryViewTest(TestCase):
    """Test cases for Category views."""
    
    @classmethod
    def setUpTestData(cls):
        """Setup data for all tests."""
        cls.category = Category.objects.create(
            name="Culture",
            description="Cultural and historical tourism",
            icon="temple_hindu"
        )
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_category_list_view_status_code(self):
        """Test category list view returns 200."""
        response = self.client.get(reverse('core:category_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_view_template(self):
        """Test category list uses correct template."""
        response = self.client.get(reverse('core:category_list'))
        self.assertTemplateUsed(response, 'core/category_list.html')
    
    def test_category_detail_view_status_code(self):
        """Test category detail view returns 200."""
        response = self.client.get(
            reverse('core:category_detail', kwargs={'slug': self.category.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_category_detail_view_template(self):
        """Test category detail uses correct template."""
        response = self.client.get(
            reverse('core:category_detail', kwargs={'slug': self.category.slug})
        )
        self.assertTemplateUsed(response, 'core/category_detail.html')


class BaseViewTest(TestCase):
    """Test cases for views in apps.base."""
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_home_view_status_code(self):
        """Test home view returns 200."""
        response = self.client.get(reverse('base:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_template(self):
        """Test home uses correct template."""
        response = self.client.get(reverse('base:home'))
        self.assertTemplateUsed(response, 'base/home.html')
    
    def test_about_view_status_code(self):
        """Test about view returns 200."""
        response = self.client.get(reverse('base:about'))
        self.assertEqual(response.status_code, 200)
    
    def test_about_view_template(self):
        """Test about uses correct template."""
        response = self.client.get(reverse('base:about'))
        self.assertTemplateUsed(response, 'base/about.html')


class SurpriseMeViewTest(TestCase):
    """Test cases for Surprise Me feature."""
    
    def setUp(self):
        """Setup client for each test."""
        self.client = Client()
    
    def test_surprise_view_status_code(self):
        """Test surprise view returns 200."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_view_template(self):
        """Test surprise uses correct template."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertTemplateUsed(response, 'core/surprise.html')
    
    def test_surprise_view_context(self):
        """Test surprise view has destination_list in context."""
        response = self.client.get(reverse('core:surprise_me'))
        self.assertIn('destination_list', response.context)


class URLRoutingTest(TestCase):
    """Test URL routing works correctly."""
    
    def test_home_url_resolves(self):
        """Test home URL is accessible."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_about_url_resolves(self):
        """Test about URL is accessible."""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
    
    def test_destination_list_url_resolves(self):
        """Test destination list URL is accessible."""
        response = self.client.get('/destinations/')
        self.assertEqual(response.status_code, 200)
    
    def test_category_list_url_resolves(self):
        """Test category list URL is accessible."""
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, 200)
    
    def test_surprise_url_resolves(self):
        """Test surprise URL is accessible."""
        response = self.client.get('/surprise/')
        self.assertEqual(response.status_code, 200)
