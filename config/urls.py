from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views
from leads.views import DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("properties.urls")),
    path("leads/", include("leads.urls")),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("signup/", accounts_views.signup, name="signup"),
    path("login/", accounts_views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
