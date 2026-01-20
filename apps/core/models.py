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
        # Override save untuk generate slug destinasi
        if not self.slug:
            base_slug = slugify(self.nama_destinasi)
            slug = base_slug
            counter = 1
            # Loop cek duplikasi slug
            while Destinasi.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        # Representasi string nama destinasi
        return self.nama_destinasi

    class Meta:
        verbose_name_plural = "Destinations"
        verbose_name = "Destination"
    
