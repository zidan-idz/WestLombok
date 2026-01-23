from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Destination List & Search
    path('destinations/', views.DestinationListView.as_view(), name='destination_list'),
    
    # Destination Detail
    path('destinations/<slug:slug>/', views.DestinationDetailView.as_view(), name='destination_detail'),

    # District Detail
    path('districts/<slug:slug>/', views.DistrictDetailView.as_view(), name='district_detail'),
    
    # Category List
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    
    # Category Detail
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),

    # Additional Features
    path('surprise/', views.surprise_me, name='surprise_me'),
]