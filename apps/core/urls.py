from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Daftar Destinasi & Pencarian
    path('destinations/', views.DestinationListView.as_view(), name='destination_list'),
    
    # Detail Destinasi
    path('destinations/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination_detail'),

    # Detail Kecamatan
    path('districts/<slug:slug>/', views.DistrictDetailView.as_view(), name='district_detail'),
    
    # Daftar Kategori
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Detail Kategori
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Fitur Tambahan
    path('surprise/', views.surprise_me, name='surprise_me'),
]