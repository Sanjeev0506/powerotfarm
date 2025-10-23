from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve as static_serve
from apps.orders import views as orders_views
from apps.contact import views as contact_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # include app-specific namespaces
    path('api/contact/', include('apps.contact.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/payments/', include('apps.payments.urls')),

    # top-level convenience endpoints used by the frontend
    path('api/products/', orders_views.list_products),
    path('api/services/', contact_views.list_services),
    path('api/gallery/', contact_views.list_gallery),
    path('api/process/', contact_views.list_process),
]

# Serve the frontend index.html at root when running in DEBUG
if settings.DEBUG:
    # Serve frontend static assets (css, js, assets/images) and top-level HTML files
    # This maps requests like /css/... /js/... /assets/... and /about.html -> <repo-root>/frontend/...
    frontend_root = str(settings.BASE_DIR.parent / 'frontend')
    urlpatterns += [
        # CSS, JS and asset directories
        re_path(r'^(?P<path>(?:css|js|assets)/.*)$', static_serve, {'document_root': frontend_root}),
        # common root-level static files (images, icons, scripts)
        re_path(r'^(?P<path>[^/]+\.(?:js|css|png|jpg|jpeg|gif|ico|svg|webp))$', static_serve, {'document_root': frontend_root}),
        # HTML pages
        re_path(r'^(?P<path>.*\.html)$', static_serve, {'document_root': frontend_root}),
    ]
    # Serve frontend index.html at site root from the frontend folder so the full static
    # SPA-style homepage is used during local development.
    urlpatterns += [
        re_path(r'^$', static_serve, {'path': 'index.html', 'document_root': frontend_root}),
    ]

# during DEBUG serve static files from STATIC_ROOT
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
