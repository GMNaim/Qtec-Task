from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('search_history.urls', namespace='search_history'))
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL,
                                       document_root=settings.STATIC_ROOT,
                                       show_indexes=True)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL,
                                       document_root=settings.MEDIA_ROOT,
                                       show_indexes=True)
