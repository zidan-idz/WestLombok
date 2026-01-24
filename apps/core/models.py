from django.db import models
from django.utils.text import slugify
from django.conf import settings


# --- 1. District Model (New Entity) ---
class District(models.Model):
    """
    Model to store District (Kecamatan) data.
    Separated from Destination to allow dynamic updates by admin.
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="District Name")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    thumbnail = models.ImageField(upload_to='districts/', blank=True, null=True, verbose_name="Thumbnail Image")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ['name']


class Category(models.Model):
    """
    Model to store tourism destination categories.
    """
    # Category name field
    name = models.CharField(max_length=100, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Category Description")
    icon = models.CharField(max_length=50, default='category', verbose_name="Icon Name", help_text="Google Material Icon Name (e.g. waves, landscape, restaurant)")
    # Slug auto-generated from category name
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def clean(self):
        # Auto-format icon setting: lowercase & replace separators with underscore (Material Icons format)
        if self.icon:
            self.icon = self.icon.lower().strip().replace(' ', '_').replace('-', '_')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Trigger validation/cleaning before save
        # Override save to auto-generate slug
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Check for duplicate slugs
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        # String representation of model
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"


class Destination(models.Model):
    """
    Model to store tourism destination details.
    """
    # Basic information
    name = models.CharField(max_length=100, verbose_name="Destination Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Description")
    
    
    # NEW District Relation
    district = models.ForeignKey(
        District, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='destinations',
        verbose_name="District"
    )

    maps_embed_url = models.CharField(max_length=300, blank=True, default='', verbose_name="Google Maps URL")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Additional Info")
    
    # Photo assets
    main_image = models.ImageField(upload_to='destinations/primary/', verbose_name="Main Photo (Hero)")
    

    # Relation to User (Manager)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='managed_destinations',
        blank=True,
        null=True,
        verbose_name="Manager"
    )
    
    # Relation to Category
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='destinations',
        blank=True,
        null=True,
        verbose_name="Category"
    )

    # Metadata
    # Standard View Count (Simple Integer)
    view_count = models.IntegerField(default=0, verbose_name="Total Views")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # 1. Auto-generate Slug
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Destination.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        # 2. Auto-Convert Google Maps Link to Embed URL for Iframe
        if self.maps_embed_url and '<iframe' in self.maps_embed_url:
            import re
            # Extract src="..." content
            match = re.search(r'src="([^"]+)"', self.maps_embed_url)
            if match:
                self.maps_embed_url = match.group(1)
                
        super().save(*args, **kwargs)

    def __str__(self):
        # String representation of destination name
        return self.name

    class Meta:
        verbose_name_plural = "Destinations"
        verbose_name = "Destination"
        ordering = ['-created_at']


# --- 2. Destination Gallery (New Entity) ---
class DestinationGallery(models.Model):
    """
    Model to store unlimited gallery images for a destination.
    """
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"


