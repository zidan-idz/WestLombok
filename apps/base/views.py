from django.shortcuts import render
from django.views.generic import TemplateView
from apps.core.models import Destination, Category
from typing import Any


class HomeView(TemplateView):
    """
    View for the homepage, displaying featured destinations & categories.
    """
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # Get standard context data from parent
        context = super().get_context_data(**kwargs)
        # Query 3 latest destinations for hero slider
        context['featured_destinations'] = Destination.objects.order_by('-created_at')[:3]
        # Query 3 most popular destinations by views
        context['popular_destinations'] = Destination.objects.order_by('-view_count')[:3]
        # Query all categories for navigation/widget
        context['category_list'] = Category.objects.all()
        return context


class AboutView(TemplateView):
    """
    View for the 'About Us' page.
    """
    template_name = 'base/about.html'


# --- Custom Error Handlers ---

def custom_404(request, exception):
    """
    Custom handler for 404 error (page not found).
    Displays 404.html with status code 404.
    """
    return render(request, '404.html', status=404)