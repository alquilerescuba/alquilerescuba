from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path("", views.PropertyListView.as_view(), name="list"),
    path("propiedad/<int:pk>/", views.PropertyDetailView.as_view(), name="detail"),
    path(
        "api/property/<int:property_id>/booked-dates/",
        views.get_booked_dates,
        name="booked-dates",
    ),
    path("propiedad/<int:pk>/valorar/", views.add_review, name="add_review"),
    # ============================================
    # NUEVAS RUTAS PARA ANFITRIONES
    # ============================================
    path("crear/", views.create_property, name="create"),
    path("mis-propiedades/", views.my_properties, name="my_properties"),
    path("editar/<int:pk>/", views.update_property, name="update"),
    path("eliminar/<int:pk>/", views.delete_property, name="delete"),
]
