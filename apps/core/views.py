from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.http import Http404
from .models import Destinasi, Kategori
from django.db.models import Q
import random

# --- List Views (Moved from Base) ---

class DestinasiListView(ListView):
    """
    View untuk menampilkan daftar semua destinasi wisata.
    Mendukung paginasi dan pencarian sederhana.
    """
    model = Destinasi
    template_name = "core/destinasi_list.html"
    context_object_name = "destinasi_list"
    paginate_by = 6 
    ordering = ['-tanggal_dibuat']

    def get_queryset(self):
        # Override query untuk fitur pencarian & filter kategori
        queryset = super().get_queryset()
        
        # Filter Pencarian (Text)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nama_destinasi__icontains=query) |
                Q(deskripsi__icontains=query) |
                Q(kecamatan__icontains=query)
            )
            
        # Filter Kategori (Dropdown)
        kategori_slug = self.request.GET.get('kategori')
        if kategori_slug:
            queryset = queryset.filter(kategori__slug=kategori_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        # Tambahkan list kategori untuk dropdown filter
        context = super().get_context_data(**kwargs)
        context['kategori_list'] = Kategori.objects.all()
        return context

class KategoriListView(ListView):
    """
    View untuk menampilkan daftar kategori destinasi.
    """
    model = Kategori
    template_name = 'core/kategori_list.html'
    context_object_name = 'kategori_list'

# --- Detail Views ---

class DestinasiDetailView(DetailView):
    """
    View untuk menampilkan detail lengkap sebuah destinasi.
    """
    model = Destinasi
    template_name = "core/destinasi_detail.html"
    context_object_name = "destinasi"
    slug_url_kwarg = "slug"

    def get_object(self):
        # Override get_object untuk menambah counter views
        obj = super().get_object()
        obj.jumlah_views += 1 
        obj.save()
        return obj

class KategoriDetailView(ListView):
    """
    View untuk menampilkan destinasi dalam kategori tertentu.
    Menampilkan 3 destinasi acak dari kategori yang dipilih.
    """
    model = Destinasi
    template_name = 'core/kategori_detail.html'
    context_object_name = 'destinasi_list'

    def get_queryset(self):
        # Error handling untuk kategori yang tidak ditemukan
        try:
            self.kategori = Kategori.objects.get(slug=self.kwargs['slug'])
        except Kategori.DoesNotExist:
            raise Http404("Kategori tidak ditemukan")
        
        # Ambil 3 destinasi acak dari kategori ini
        return Destinasi.objects.filter(kategori=self.kategori).order_by('?')[:3]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kategori'] = self.kategori
        return context

# --- Feature Views ---

def surprise_me(request):
    """
    Fitur 'Surprise Me', menampilkan destinasi secara acak untuk inspirasi.
    """
    # Ambil data spesifik untuk efisiensi
    destinasi_list = list(Destinasi.objects.all().values('nama_destinasi', 'kecamatan', 'foto_utama', 'slug'))
    # Acak urutan list
    random.shuffle(destinasi_list)
    return render(request, 'core/surprise.html', {'destinasi_list': destinasi_list})