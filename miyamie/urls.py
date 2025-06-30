from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
      path('admin/', admin.site.urls),
      path("__reload__/", include("django_browser_reload.urls")),
      path('', include('website.urls')),
      path("ckeditor5/", include('django_ckeditor_5.urls')),
      path('i18n/', include('django.conf.urls.i18n')),  # Ovo omogućava promenu jezika
  ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += i18n_patterns(
    path('', include('website.urls')),
    prefix_default_language=True,  # Ako ne želiš /en/ u URL-u za podrazumevani jezik
)