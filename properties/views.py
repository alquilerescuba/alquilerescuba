from django.views.generic import ListView, DetailView
from django_filters.views import FilterView  # ✅ ESTA LÍNEA ES LA QUE FALTA
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from properties.models import Property, Booking
from properties.filters import PropertyFilter
from datetime import timedelta
from django.shortcuts import render


class PropertyListView(FilterView):
    model = Property
    template_name = "properties/list.html"
    context_object_name = "properties"
    filterset_class = PropertyFilter
    paginate_by = 12

    def get_queryset(self):
        return Property.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Los métodos average_rating y reviews_count ya están en el modelo
        return context


from django.db.models import Avg  # Añade esta importación al inicio


class PropertyDetailView(DetailView):
    model = Property
    template_name = "properties/detail.html"
    context_object_name = "property"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_properties"] = Property.objects.filter(
            location=self.object.location, is_active=True
        ).exclude(id=self.object.id)[:3]

        from django.conf import settings

        context["business_whatsapp"] = settings.BUSINESS_WHATSAPP

        # Calcular promedio de valoraciones
        reviews = self.object.reviews.all()
        if reviews.exists():
            context["average_rating"] = reviews.aggregate(Avg("rating"))["rating__avg"]
            context["total_reviews"] = reviews.count()
        else:
            context["average_rating"] = 0
            context["total_reviews"] = 0

        # Para saber si el usuario ya valoró esta propiedad
        if self.request.user.is_authenticated:
            context["user_reviewed"] = reviews.filter(user=self.request.user).exists()
        else:
            context["user_reviewed"] = False

        return context


@require_GET
def get_booked_dates(request, property_id):
    """API para obtener fechas ocupadas de una propiedad"""
    try:
        property = Property.objects.get(id=property_id)
        bookings = Booking.objects.filter(property=property)

        print(f"Propiedad: {property.title}")
        print(f"Reservas encontradas: {bookings.count()}")

        # Generar lista de fechas ocupadas
        booked_dates = []
        for booking in bookings:
            print(f"Reserva: {booking.start_date} a {booking.end_date}")

            # Crear rango de fechas (incluyendo ambos extremos)
            current = booking.start_date
            while current <= booking.end_date:
                booked_dates.append(current.strftime("%Y-%m-%d"))
                current += timedelta(days=1)

        print(f"Total fechas ocupadas: {len(booked_dates)}")
        print(f"Primeras 5: {booked_dates[:5]}")

        return JsonResponse(
            {"booked_dates": booked_dates, "success": True, "count": len(booked_dates)}
        )

    except Property.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "Propiedad no encontrada"}, status=404
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Review
from .forms import ReviewForm


@login_required
def add_review(request, pk):  # Cambia property_id por pk
    property = get_object_or_404(Property, id=pk)

    # Verificar si el usuario ya valoró esta propiedad
    if Review.objects.filter(property=property, user=request.user).exists():
        messages.error(request, "Ya has valorado esta propiedad anteriormente.")
        return redirect("properties:detail", pk=pk)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.property = property
            review.user = request.user
            review.save()
            messages.success(request, "¡Gracias por tu valoración!")
            return redirect("properties:detail", pk=pk)
    else:
        form = ReviewForm()

    return render(
        request, "properties/add_review.html", {"form": form, "property": property}
    )
