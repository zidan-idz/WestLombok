from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import Category, Destination, District, DestinationGallery

@admin.register(District)
class DistrictAdmin(ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)

class DestinationGalleryInline(TabularInline):
    model = DestinationGallery
    extra = 1
    fields = ('image', 'caption')

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    # Konfigurasi Admin untuk model Kategori dengan Unfold.
    list_display = ('name', 'slug', 'icon_preview')
    exclude = ['slug']  # Sembunyikan slug (otomatis)
    list_per_page = 20
    search_fields = ('name',)
    list_filter_submit = True

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Link bantuan untuk Google Icons
        if db_field.name == 'icon':
            kwargs['help_text'] = format_html(
                'Pilih nama ikon dari <a href="https://fonts.google.com/icons" target="_blank" class="text-blue-600 hover:text-blue-800 underline">Google Material Icons</a> (cth: <code>hiking</code>, <code>restaurant</code>, <code>waves</code>) dan tempel di sini.'
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

    def destination_count_badge(self, obj):
        # Tampilkan badge jumlah destinasi
        count = obj.destinations.count()
        color = "green" if count > 0 else "gray"
        return format_html(
            '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{}-100 text-{}-800">{} Destinations</span>',
            color, color, count
        )
    destination_count_badge.short_description = "Total Destinations"


@admin.register(Destination)
class DestinationAdmin(ModelAdmin):
    # Konfigurasi Admin Destinasi dengan preview gambar & badge.
    list_display = ('image_preview', 'name', 'category_badge', 'district', 'view_count', 'created_at')
    list_per_page = 15
    search_fields = ('name', 'district__name', 'manager__username')
    list_filter = ('district', 'category')
    list_filter_submit = True
    exclude = ['manager', 'slug']
    readonly_fields = ['view_count', 'created_at']
    
    # Inline Gallery
    inlines = [DestinationGalleryInline]

    # Set field order in edit form
    fields = [
        'name',
        'description',
        'district', # FK ke Model District
        'category',
        'maps_embed_url',
        'main_image',
        'view_count',
        'created_at'
    ]

    def save_model(self, request, obj, form, change):
        if not obj.manager:
            obj.manager = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'maps_embed_url':
            kwargs['help_text'] = format_html(
                'Buka Google Maps -> Bagikan -> <strong>Sematkan peta</strong> -> Salin HTML. Tempel kode <code>&lt;iframe...&gt;</code> lengkap di sini. Kami akan ekstrak link-nya otomatis.'
            )
        return super().formfield_for_dbfield(db_field, **kwargs)
    
    def image_preview(self, obj):
        if obj.main_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" />',
                obj.main_image.url
            )
        return "-"
    image_preview.short_description = "Photo"

    def category_badge(self, obj):
        if obj.category:
            return format_html(
                '<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">{}</span>',
                obj.category.name
            )
        return "-"
    category_badge.short_description = "Category"
