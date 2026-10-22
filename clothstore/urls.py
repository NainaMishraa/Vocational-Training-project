"""
URL configuration for clothstore project.

CONCEPT 8 (NAMED URLS & URL DISPATCHER):
The project-level urls.py delegates store-related URLs to the store app's urls.py
using the include() function.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Delegate all root URLs to store app
    path('', include('store.urls')),
]

# CONCEPT 12 (STATIC + MEDIA):
# In development (DEBUG = True), Django development server needs explicit URL patterns
# to serve media files uploaded to MEDIA_ROOT.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
