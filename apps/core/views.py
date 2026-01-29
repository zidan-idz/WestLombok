from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.db.models import F
from .models import Destination, Category, District
from django.db.models import Q
import random


# --- List Views ---

class DestinationListView(ListView):
    # Menampilkan daftar seluruh destinasi wisata.
    # Mendukung paginasi dan pencarian sederhana.
    model = Destination
    template_name = "core/destination_list.html"
    context_object_name = "destination_list"
    paginate_by = 6 
    ordering = ['-created_at']

    def get_queryset(self):
        # Override query untuk fitur cari & filter kategori
        queryset = super().get_queryset()
        
        # Filter Pencarian Teks
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(district__name__icontains=query)
            )
            
        # Filter Dropdown Kategori
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        # Data kategori untuk dropdown filter
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryListView(ListView):
    # Menampilkan daftar kategori wisata.
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'category_list'


# --- Detail Views ---

class DestinationDetailView(DetailView):
    # Menampilkan detail lengkap destinasi.
    model = Destination
    template_name = "core/destination_detail.html"
    context_object_name = "destination"
    slug_url_kwarg = "slug"

    def get_object(self):
        # Override get_object untuk tambah counter views secara atomik
        obj = super().get_object()
        # Update atomik untuk performa lebih baik
        Destination.objects.filter(pk=obj.pk).update(
            view_count=F('view_count') + 1
        )
        obj.refresh_from_db()
        return obj

class DistrictDetailView(DetailView):
    # Menampilkan detail Kecamatan dan destinasinya.
    model = District
    template_name = "core/district_detail.html"
    context_object_name = "district"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ambil semua destinasi dalam kecamatan ini
        context['destination_list'] = self.object.destinations.all()
        return context

class CategoryDetailView(ListView):
    # Menampilkan destinasi dalam kategori spesifik.
    model = Destination
    template_name = 'core/category_detail.html'
    context_object_name = 'destination_list'

    def get_queryset(self):
        # Error handling jika kategori tidak ditemukan
        try:
            self.category = Category.objects.get(slug=self.kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404("Category not found")
        
        # Ambil destinasi dari kategori ini, urut dari yang terbaru
        return Destination.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# --- Feature Views ---

def surprise_me(request):
    # Fitur 'Surprise Me', menampilkan destinasi acak untuk inspirasi.
    # Logika: Ambil semua data lalu acak
    # Memastikan klien mendapatkan dataset penuh untuk animasi
    destination_list = list(Destination.objects.all().values('name', 'district__name', 'main_image', 'slug'))
    random.shuffle(destination_list)
    return render(request, 'core/surprise.html', {'destination_list': destination_list})