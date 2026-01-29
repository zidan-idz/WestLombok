from django.db import models
from django.utils.text import slugify
from django.conf import settings


# --- 1. Model Kecamatan (Entitas Baru) ---
class District(models.Model):
    # Menyimpan data Kecamatan untuk pembaruan dinamis admin.
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Kecamatan")
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    thumbnail = models.ImageField(upload_to='districts/', blank=True, null=True, verbose_name="Gambar Thumbnail")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kecamatan"
        verbose_name_plural = "Kecamatan"
        ordering = ['name']


class Category(models.Model):
    # Model untuk menyimpan kategori wisata.
    # Nama kategori
    name = models.CharField(max_length=100, verbose_name="Nama Kategori")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi Kategori")
    icon = models.CharField(max_length=50, default='category', verbose_name="Nama Ikon", help_text="Google Material Icon Name (contoh: waves, landscape, restaurant)")
    # Slug otomatis dari nama kategori
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def clean(self):
        # Format otomatis ikon: huruf kecil & ganti spasi jadi underscore
        if self.icon:
            self.icon = self.icon.lower().strip().replace(' ', '_').replace('-', '_')
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Validasi sebelum simpan
        # Override save untuk buat slug otomatis
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            # Cek duplikasi slug
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        # Representasi string model
        return self.name

    class Meta:
        verbose_name_plural = "Kategori"
        verbose_name = "Kategori"


class Destination(models.Model):
    # Model untuk menyimpan detail destinasi wisata.
    # Informasi dasar
    name = models.CharField(max_length=100, verbose_name="Nama Destinasi")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi")
    
    
    # Relasi ke Kecamatan (Baru)
    district = models.ForeignKey(
        District, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='destinations',
        verbose_name="Kecamatan"
    )

    maps_embed_url = models.CharField(max_length=300, blank=True, default='', verbose_name="URL Google Maps")
    additional_info = models.TextField(blank=True, null=True, verbose_name="Info Tambahan")
    
    # Aset foto
    main_image = models.ImageField(upload_to='destinations/primary/', verbose_name="Foto Utama (Hero)")
    

    
    # Relasi ke User (Pengelola)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='managed_destinations',
        blank=True,
        null=True,
        verbose_name="Pengelola" 
    )
    
    
    # Relasi ke Kategori
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='destinations',
        blank=True,
        null=True,
        verbose_name="Kategori"
    )

    # Metadata
    # Penghitung tayangan (Integer sederhana)
    view_count = models.IntegerField(default=0, verbose_name="Total Dilihat")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # 1. Buat Slug otomatis
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Destination.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
            
        # 2. Konversi Link Google Maps ke Embed URL
        if self.maps_embed_url and '<iframe' in self.maps_embed_url:
            import re
            # Ambil konten src="..."
            match = re.search(r'src="([^"]+)"', self.maps_embed_url)
            if match:
                self.maps_embed_url = match.group(1)
                
        super().save(*args, **kwargs)

    def __str__(self):
        # Representasi string nama destinasi
        return self.name

    class Meta:
        verbose_name_plural = "Destinasi"
        verbose_name = "Destinasi"
        ordering = ['-created_at']


# --- 2. Galeri Destinasi (Entitas Baru) ---
class DestinationGallery(models.Model):
    # Model menyimpan galeri foto tak terbatas untuk destinasi.
    destination = models.ForeignKey(Destination, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Gambar Galeri"
        verbose_name_plural = "Gambar Galeri"


