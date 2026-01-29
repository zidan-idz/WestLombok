# Konfigurasi URL utama untuk proyek.
# Mengatur routing ke admin, apps base, core, dan media files.
from django.contrib import admin
from django.urls import path, include
# Tambahan import untuk media
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.base.urls')),
    path('', include('apps.core.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')

# Custom error handlers
handler404 = 'apps.base.views.custom_404'