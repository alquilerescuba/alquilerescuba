from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from accounts import views as accounts_views
from leads.views import DashboardView
from properties.sitemaps import PropertySitemap

# Configuración del diccionario de sitemaps
sitemaps = {
    "properties": PropertySitemap,
}


# Función para generar el robots.txt dinámicamente
def robots_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Sitemap: http://dea4ever.net",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


urlpatterns = [
    path("admin/", admin.site.urls),
    # RUTA PARA ROBOTS.TXT (Prioridad alta)
    path("robots.txt", robots_txt),
    # RUTA PARA EL SITEMAP (Prioridad alta)
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # PROPIEDADES E INCLUDES (Se mueven abajo para no interceptar sitemap.xml)
    path("", include("properties.urls")),
    path("leads/", include("leads.urls")),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("signup/", accounts_views.signup, name="signup"),
    path("login/", accounts_views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
