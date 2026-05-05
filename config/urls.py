from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap  # <--- IMPORTANTE
from accounts import views as accounts_views
from leads.views import DashboardView
from properties.sitemaps import PropertySitemap  # <--- IMPORTANTE

# Configuración del diccionario de sitemaps
sitemaps = {
    "properties": PropertySitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("properties.urls")),
    path("leads/", include("leads.urls")),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("signup/", accounts_views.signup, name="signup"),
    path("login/", accounts_views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    # RUTA PARA GOOGLE
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
