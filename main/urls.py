from django.urls import path, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url, include

from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.static import serve


handler404 = 'store.views.page_not_found'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='accounts')),
    
    path('', views.home, name='home'),
    path('froala_editor/', include('froala_editor.urls')),
    
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    url(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns