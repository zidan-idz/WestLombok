from django.shortcuts import render
from django.views.generic import TemplateView
from apps.core.models import Destinasi, Kategori
from typing import Any

class HomeView(TemplateView):
    """
    View untuk halaman utama (homepage), menampilkan destinasi unggulan & kategori.
    """
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Ambil context data standar dari parent
        context = super().get_context_data(**kwargs)
        # Query 3 destinasi terbaru untuk slider hero
        context['featured_destinasi'] = Destinasi.objects.order_by('-tanggal_dibuat')[:3]
        # Query 3 destinasi paling populer berdasarkan views
        context['popular_destinasi'] = Destinasi.objects.order_by('-jumlah_views')[:3]
        # Query semua kategori untuk navigasi/widget
        context['kategori_list'] = Kategori.objects.all()
        return context

class AboutView(TemplateView):
    """
    View untuk halaman 'Tentang Kami'.
    """
    template_name = 'base/about.html'


# --- Custom Error Handlers ---

def custom_404(request, exception):
    """
    Custom handler untuk error 404 (halaman tidak ditemukan).
    Menampilkan halaman 404.html dengan status code 404.
    """
    return render(request, '404.html', status=404)