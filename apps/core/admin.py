from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Kategori, Destinasi

@admin.register(Kategori)
class KategoriAdmin(ModelAdmin):
    """
    Konfigurasi Admin untuk model Kategori menggunakan Unfold.
    """
    list_display = ('nama_kategori', 'slug', 'icon_preview')
    # prepopulated_fields = {'slug': ('nama_kategori',)} # Disable manual slug
    exclude = ['slug'] # Hide slug
    list_per_page = 20
    search_fields = ('nama_kategori',)
    list_filter_submit = True  # Tampilkan tombol submit filter

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Helper link Google Icons
        if db_field.name == 'icon':
            kwargs['help_text'] = format_html(
                'Pick an icon name from <a href="https://fonts.google.com/icons" target="_blank" class="text-blue-600 hover:text-blue-800 underline">Google Material Icons</a> (e.g. <code>hiking</code>, <code>restaurant</code>, <code>waves</code>) and paste it here.'
            )
        return super().formfield_for_dbfield(db_field, **kwargs)

    class Media:
        css = {
            'all': ('https://fonts.googleapis.com/icon?family=Material+Icons',)
        }

    def icon_preview(self, obj):
        if obj.icon:
            return format_html(
                '<span class="material-icons text-gray-600" style="font-size: 28px;">{}</span>',
                obj.icon
            )
        return "-"
    icon_preview.short_description = "Icon"

    def destinasi_count_badge(self, obj):
        # Menampilkan badge jumlah detinasi
        count = obj.destinasi.count()
        color = "green" if count > 0 else "gray"
        return format_html(
            '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{}-100 text-{}-800">{} Destinations</span>',
            color, color, count
        )
    destinasi_count_badge.short_description = "Total Destinations"

@admin.register(Destinasi)
class DestinasiAdmin(ModelAdmin):
    """
    Konfigurasi Admin untuk model Destinasi dengan fitur preview gambar & badge.
    """
    list_display = ('image_preview', 'nama_destinasi', 'kategori_badge', 'kecamatan', 'jumlah_views', 'tanggal_dibuat')
    # prepopulated_fields = {'slug': ('nama_destinasi',)} # Disable manual slug
    list_per_page = 15
    search_fields = ('nama_destinasi', 'kecamatan', 'pengelola__username')
    list_filter_submit = True
    exclude = ['pengelola', 'slug'] # Hide slug & pengelola
    readonly_fields = ['jumlah_views', 'tanggal_dibuat']
    
    # Atur urutan field di form edit
    fields = [
        'nama_destinasi',
        'deskripsi',
        'kecamatan',
        'kategori',  # Pindahkan ke sini (di bawah kecamatan)
        'lokasi_maps',
        'foto_utama',
        'foto_lainnya_1',
        'foto_lainnya_2',
        'foto_lainnya_3',
        'foto_lainnya_4',
        'jumlah_views', # Tampilkan tapi readonly
        'tanggal_dibuat'
    ]

    def save_model(self, request, obj, form, change):
        # Auto-assign pengelola jika belum ada
        if not obj.pengelola:
            obj.pengelola = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Helper link Google Maps
        if db_field.name == 'lokasi_maps':
            kwargs['help_text'] = format_html(
                'Go to Google Maps -> Share -> <strong>Embed a map</strong> -> Copy HTML. Paste the full <code>&lt;iframe...&gt;</code> code here. We will extract the link automatically.'
            )
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    # Fungsi Preview Gambar
    def image_preview(self, obj):
        if obj.foto_utama:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />',
                obj.foto_utama.url
            )
        return "-"
    image_preview.short_description = "Photo"

    # Badge Warna untuk Kategori
    def kategori_badge(self, obj):
        if obj.kategori:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{}</span>',
                obj.kategori.nama_kategori
            )
        return "-"
    kategori_badge.short_description = "Category"

