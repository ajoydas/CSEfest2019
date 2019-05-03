
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('kora_fest/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
    path('', include('puzzle.urls', namespace='puzzle')),
]

# handler500 = 'puzzle.views.hacker_man'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
