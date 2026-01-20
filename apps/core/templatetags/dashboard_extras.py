from django import template
from apps.core.models import Destinasi, Kategori
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_destinasi_count():
    return Destinasi.objects.count()

@register.simple_tag
def get_kategori_count():
    return Kategori.objects.count()

@register.simple_tag
def get_user_count():
    return User.objects.count()

import json
from django.utils.safestring import mark_safe

@register.simple_tag
def get_top_destinations_json():
    # Ambil top 5 destinasi berdasarkan views
    top_destinasi = Destinasi.objects.order_by('-jumlah_views')[:5]
    
    data = {
        'labels': [d.nama_destinasi for d in top_destinasi],
        'data': [d.jumlah_views for d in top_destinasi],
    }
    return mark_safe(json.dumps(data))

@register.simple_tag
def get_recent_destinations():
    # Ambil 5 destinasi terbaru berdasarkan tanggal dibuat
    return Destinasi.objects.order_by('-tanggal_dibuat')[:5]
