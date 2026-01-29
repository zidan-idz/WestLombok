from django.shortcuts import render
from django.views.generic import TemplateView
from apps.core.models import Destination, Category, District
from django.db.models import Sum
from typing import Any


class HomeView(TemplateView):
    # View homepage, menampilkan destinasi unggulan & kategori.
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Ambil context data standar dari parent
        context = super().get_context_data(**kwargs)
        # Query 3 destinasi terbaru untuk slider hero
        context['featured_destinations'] = Destination.objects.order_by('-created_at')[:3]
        # Query 3 destinasi terpopuler berdasarkan views
        context['popular_destinations'] = Destination.objects.order_by('-view_count')[:3]
        # Query semua kategori untuk navigasi/widget
        context['category_list'] = Category.objects.all()
        # Statistik untuk homepage
        context['destination_count'] = Destination.objects.count()
        context['district_count'] = District.objects.count()
        context['total_views'] = Destination.objects.aggregate(Sum('view_count'))['view_count__sum'] or 0
        return context


class AboutView(TemplateView):
    # View untuk halaman 'Tentang Kami'.
    template_name = 'base/about.html'


# --- Custon Error Handlers ---

def custom_404(request, exception):
    # Handler kustom untuk error 404 (halaman tidak ditemukan).
    # Menampilkan 404.html dengan status code 404.
    return render(request, '404.html', status=404)