from core import urls, views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("admin/logout/", auth_views.LogoutView.as_view(), name="admin_logout"),
        path(
            "enviar_email_suporte/",
            views.enviar_email_suporte,
            name="enviar_email_suporte",
        ),
        path("", include("core.urls")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
