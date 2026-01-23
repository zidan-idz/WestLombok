from django import template
from apps.core.models import Destination, Category
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_destination_count():
    return Destination.objects.count()

@register.simple_tag
def get_category_count():
    return Category.objects.count()

@register.simple_tag
def get_user_count():
    return User.objects.count()

import json
from django.utils.safestring import mark_safe

@register.simple_tag
def get_top_destinations_json():
    # Get top 5 destinations by views
    top_destinations = Destination.objects.order_by('-view_count')[:5]
    
    data = {
        'labels': [d.name for d in top_destinations],
        'data': [d.view_count for d in top_destinations],
    }
    return mark_safe(json.dumps(data))

@register.simple_tag
def get_recent_destinations():
    # Get 5 most recent destinations by creation date
    return Destination.objects.order_by('-created_at')[:5]
