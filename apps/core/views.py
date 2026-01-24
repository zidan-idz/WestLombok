from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
from django.http import Http404
from django.db.models import F
from .models import Destination, Category, District
from django.db.models import Q
import random


# --- List Views ---

class DestinationListView(ListView):
    """
    View to display list of all tourism destinations.
    Supports pagination and simple search.
    """
    model = Destination
    template_name = "core/destination_list.html"
    context_object_name = "destination_list"
    paginate_by = 6 
    ordering = ['-created_at']

    def get_queryset(self):
        # Override query for search & category filter features
        queryset = super().get_queryset()
        
        # Text Search Filter
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(district__name__icontains=query)
            )
            
        # Category Dropdown Filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        # Add category list for filter dropdown
        context = super().get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        return context


class CategoryListView(ListView):
    """
    View to display list of destination categories.
    """
    model = Category
    template_name = 'core/category_list.html'
    context_object_name = 'category_list'


# --- Detail Views ---

class DestinationDetailView(DetailView):
    """
    View to display full details of a destination.
    """
    model = Destination
    template_name = "core/destination_detail.html"
    context_object_name = "destination"
    slug_url_kwarg = "slug"

    def get_object(self):
        # Override get_object to increment view counter atomically
        obj = super().get_object()
        # Atomic update for better performance
        Destination.objects.filter(pk=obj.pk).update(
            view_count=F('view_count') + 1
        )
        obj.refresh_from_db()
        return obj

class DistrictDetailView(DetailView):
    """
    View to display details of a District and its destinations.
    """
    model = District
    template_name = "core/district_detail.html"
    context_object_name = "district"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get all destinations in this district
        context['destination_list'] = self.object.destinations.all()
        return context

class CategoryDetailView(ListView):
    """
    View to display destinations in a specific category.
    Shows 3 random destinations from the selected category.
    """
    model = Destination
    template_name = 'core/category_detail.html'
    context_object_name = 'destination_list'

    def get_queryset(self):
        # Error handling for category not found
        try:
            self.category = Category.objects.get(slug=self.kwargs['slug'])
        except Category.DoesNotExist:
            raise Http404("Category not found")
        
        # Get 3 random destinations from this category
        # Show all destinations in this category, ordered by newest
        return Destination.objects.filter(category=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# --- Feature Views ---

def surprise_me(request):
    """
    'Surprise Me' feature, displays random destinations for inspiration.
    """
    # Reverted to original logic: Fetch all and shuffle
    # This ensures clients have full dataset for animation
    destination_list = list(Destination.objects.all().values('name', 'district__name', 'main_image', 'slug'))
    random.shuffle(destination_list)
    return render(request, 'core/surprise.html', {'destination_list': destination_list})