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
]
