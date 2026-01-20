from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Daftar Destinasi & Pencarian
    path('destinasi/', views.DestinasiListView.as_view(), name='destinasi_list'),
    
    # Detail Destinasi
    path('destinasi/<slug:slug>/', views.DestinasiDetailView.as_view(), name='destinasi_detail'),
    
    # Daftar Kategori
    path('kategori/', views.KategoriListView.as_view(), name='kategori_list'),
    
    # Detail Kategori
    path('kategori/<slug:slug>/', views.KategoriDetailView.as_view(), name='kategori_detail'),

    # Fitur Tambahan
    path('surprise/', views.surprise_me, name='surprise_me'),
]