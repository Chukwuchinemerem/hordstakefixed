from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Serve media files in ALL environments (DEBUG=True or False)
# This works on Render disk because we serve directly from MEDIA_ROOT
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
        'show_indexes': False,
    }),
]
