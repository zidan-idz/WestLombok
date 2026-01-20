from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    # Halaman Utama
    path('', views.HomeView.as_view(), name='home'),
    # Halaman Tentang Kami
    path('about/', views.AboutView.as_view(), name='about'),
]