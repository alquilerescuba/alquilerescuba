from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("track/", views.track_lead, name="track"),
]
