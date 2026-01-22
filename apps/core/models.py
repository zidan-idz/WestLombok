from django.db import models
from django.utils.text import slugify
from django.conf import settings

class Kategori(models.Model):
    """
    Model untuk menyimpan kategori destinasi wisata.
    """
    # Kolom untuk nama kategori
    nama_kategori = models.CharField(max_length=100, verbose_name="Category Name")
    deskripsi = models.TextField(blank=True, null=True, verbose_name="Category Description")
    icon = models.CharField(max_length=50, default='category', verbose_name="Icon Name", help_text="Google Material Icon Name (e.g. waves, landscape, restaurant)")
    # Slug otomatis dari nama kategori
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def clean(self):
        # Auto-format icon setting: lowercase & replace separators with underscore (Material Icons format)
        if self.icon:
            self.icon = self.icon.lower().strip().replace(' ', '_').replace('-', '_')
    
    def save(self, *args, **kwargs):
        self.full_clean() # Trigger validation/cleaning before save
        # Override save untuk generate slug otomatis
        if not self.slug:
            base_slug = slugify(self.nama_kategori)
            slug = base_slug
            counter = 1
            # Cek duplikasi slug
            while Kategori.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Representasi string model
        return self.nama_kategori

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"

class Destinasi(models.Model):
    """
    Model untuk menyimpan detail destinasi wisata.
    """
    # Pilihan Kecamatan di Lombok Barat
    KECAMATAN_CHOICES = [
        ('Sekotong', 'Sekotong'),
        ('Lembar', 'Lembar'),
        ('Gerung', 'Gerung'),
        ('Labuapi', 'Labuapi'),
        ('Kediri', 'Kediri'),
        ('Kuripan', 'Kuripan'),
        ('Narmada', 'Narmada'),
        ('Lingsar', 'Lingsar'),
        ('Gunung Sari', 'Gunung Sari'),
        ('Batu Layar', 'Batu Layar'),
    ]

    # Informasi dasar
    nama_destinasi = models.CharField(max_length=100, verbose_name="Destination Name")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    deskripsi = models.TextField(verbose_name="Description")
    kecamatan = models.CharField(max_length=100, choices=KECAMATAN_CHOICES, verbose_name="District")
    lokasi_maps = models.CharField(max_length=300, verbose_name="Google Maps URL")
    info_tambahan = models.TextField(blank=True, null=True, verbose_name="Additional Info")
    
    # Asset foto
    foto_utama = models.ImageField(upload_to='destinations/primary/', verbose_name="Main Photo (Hero)")
    foto_lainnya_1 = models.ImageField(upload_to='destinations/secondary/', blank=True, null=True, verbose_name="Gallery Photo 1")
    foto_lainnya_2 = models.ImageField(upload_to='destinations/secondary/', blank=True, null=True, verbose_name="Gallery Photo 2")
    foto_lainnya_3 = models.ImageField(upload_to='destinations/secondary/', blank=True, null=True, verbose_name="Gallery Photo 3")
    foto_lainnya_4 = models.ImageField(upload_to='destinations/secondary/', blank=True, null=True, verbose_name="Gallery Photo 4")

    # Relasi ke User (Pengelola)
    pengelola = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='destinasi_dikelola',
        blank=True,
        null=True,
        verbose_name="Manager"
    )
    
    # Relasi ke Kategori
    kategori = models.ForeignKey(
        Kategori,
        on_delete=models.SET_NULL,
        related_name='destinasi',
        blank=True,
        null=True,
        verbose_name="Category"
    )

    # Metadata
    jumlah_views = models.IntegerField(default=0, verbose_name="Total Views")
    tanggal_dibuat = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # 1. Generate Slug Otomatis
        if not self.slug:
            base_slug = slugify(self.nama_destinasi)
            slug = base_slug
            counter = 1
            while Destinasi.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        # 2. Auto-Convert Google Maps Link to Embed URL for Iframe
        # Support formats:
        # - https://goo.gl/maps/... (Short) -> Warning: Short links hard to resolve without request, but we can try basic iframe logic or instruct user
        # - https://www.google.com/maps/place/... 
        # - https://maps.app.goo.gl/...
        # Target Embed Format: https://www.google.com/maps/embed?pb=... (This is hard to get from regular link without API)
        # BETTER APPROACH: Use the 'q' (query) param for embed API if we don't have the explicit embed code.
        # However, the simple embed mode: https://www.google.com/maps/embed/v1/place?key=... requires API Key.
        # The implicit iframe src usually looks like: https://www.google.com/maps/embed?pb=!1m18!...
        
        # LOGIC CHANGE: Since we can't easily convert a "Share Link" to an "Embed PB Code" without scraping or API, 
        # we will rely on a safer fallback:
        # If the user provides a full 'src="..."' string strings, extract the URL.
        # If it's a raw link, we trust the user or provide a field specifically for the "Embed Map HTML" in admin.
        
        # REVISED PLAN for robustness as requested:
        # Since parsing 'pb' codes from short links is unreliable, we will assume the input MIGHT be an iframe tag copied from maps.
        # We will strip valid src from it, OR if it's a direct link, we leave it (and hope it is an embed link).
        # Actually, let's look for 'src="' pattern if the user pasted the full iframe code.
        
        if self.lokasi_maps and '<iframe' in self.lokasi_maps:
            import re
            # Extract src="..." content
            match = re.search(r'src="([^"]+)"', self.lokasi_maps)
            if match:
                self.lokasi_maps = match.group(1)
                
        super().save(*args, **kwargs)

    def __str__(self):
        # Representasi string nama destinasi
        return self.nama_destinasi

    class Meta:
        verbose_name_plural = "Destinations"
        verbose_name = "Destination"
    
