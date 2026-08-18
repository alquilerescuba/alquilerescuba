from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json
from .models import Lead
from properties.models import Property
from django.db.models import Count, Sum


@require_POST
@csrf_exempt
def track_lead(request):
    try:
        data = json.loads(request.body)
        property_id = data.get("property_id")
        check_in = data.get("check_in")
        check_out = data.get("check_out")

        if property_id:
            from leads.models import Reservation

            Reservation.objects.create(
                property_id=property_id,
                check_in=check_in,
                check_out=check_out,
                ip_address=request.META.get("REMOTE_ADDR"),
                status="pending",
            )
            return JsonResponse({"status": "ok"})
    except Exception as e:
        print(f"Error al crear reserva: {e}")

    return JsonResponse({"status": "error"}, status=400)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        # Cualquier usuario staff (dueño incluido) puede ver el dashboard
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from leads.models import Reservation
        from properties.models import Property

        # ============================================
        # 1. Resumen general con estados
        # ============================================
        total_reservations = Reservation.objects.count()
        pending = Reservation.objects.filter(status="pending").count()
        confirmed = Reservation.objects.filter(status="confirmed").count()
        completed = Reservation.objects.filter(status="completed").count()
        cancelled = Reservation.objects.filter(status="cancelled").count()

        context["total_reservations"] = total_reservations
        context["pending"] = pending
        context["confirmed"] = confirmed
        context["completed"] = completed
        context["cancelled"] = cancelled

        # ============================================
        # 2. Comisiones
        # ============================================
        completed_reservations = Reservation.objects.filter(status="completed")
        total_commission_paid = completed_reservations.filter(
            commission_paid=True
        ).count()
        total_commission_amount = (
            completed_reservations.aggregate(total=Sum("amount_paid"))["total"] or 0
        )

        context["total_commission_paid"] = total_commission_paid
        context["total_commission_amount"] = total_commission_amount

        # ============================================
        # 3. Propiedades activas
        # ============================================
        total_properties = Property.objects.filter(is_active=True).count()
        context["total_properties"] = total_properties

        # ============================================
        # 4. Reservas por ubicación
        # ============================================
        location_names = dict(Property.LOCATIONS)
        reservations_by_location = (
            Reservation.objects.values("property__location")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        for item in reservations_by_location:
            item["location_name"] = location_names.get(
                item["property__location"], item["property__location"]
            )
        context["reservations_by_location"] = reservations_by_location

        # ============================================
        # 5. Propiedades por ubicación
        # ============================================
        properties_by_location = (
            Property.objects.filter(is_active=True)
            .values("location")
            .annotate(total=Count("id"))
            .order_by("-total")
        )
        for item in properties_by_location:
            item["location_name"] = location_names.get(
                item["location"], item["location"]
            )
        context["properties_by_location"] = properties_by_location

        # ============================================
        # 6. Reservas por mes (últimos 6 meses)
        # ============================================
        six_months_ago = timezone.now() - timedelta(days=180)
        reservations_by_month = (
            Reservation.objects.filter(clicked_at__gte=six_months_ago)
            .annotate(month=TruncMonth("clicked_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        months = []
        counts = []
        for item in reservations_by_month:
            if item["month"]:
                months.append(item["month"].strftime("%b %Y"))
                counts.append(item["total"])

        context["months"] = months
        context["reservations_counts"] = counts

        # ============================================
        # 7. Top 5 propiedades con más reservas
        # ============================================
        top_properties = (
            Reservation.objects.values("property__title", "property__location")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )
        for item in top_properties:
            item["location_name"] = location_names.get(
                item["property__location"], item["property__location"]
            )
        context["top_properties"] = top_properties

        # ============================================
        # 8. Últimas 10 reservas
        # ============================================
        recent_reservations = Reservation.objects.all().order_by("-clicked_at")[:10]
        context["recent_reservations"] = recent_reservations

        return context
