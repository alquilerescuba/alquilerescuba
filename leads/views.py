from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncMonth
from django.db.models import Count, Q
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
                source="internal",
            )
            return JsonResponse({"status": "ok"})
    except Exception as e:
        print(f"Error al crear reserva: {e}")

    return JsonResponse({"status": "error"}, status=400)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from leads.models import Reservation
        from properties.models import Property

        today = timezone.now().date()

        # ============================================
        # 1. TODAS las reservas (sin filtrar por activas)
        # ============================================
        all_reservations = Reservation.objects.filter(source="internal")

        total = all_reservations.count()
        pending = all_reservations.filter(status="pending").count()
        confirmed = all_reservations.filter(status="confirmed").count()
        completed = all_reservations.filter(status="completed").count()
        cancelled = all_reservations.filter(status="cancelled").count()

        context["total_reservations"] = total
        context["pending"] = pending
        context["confirmed"] = confirmed
        context["completed"] = completed
        context["cancelled"] = cancelled

        # ============================================
        # 2. Reservas agrupadas por mes (TODAS)
        # ============================================
        from django.db.models.functions import TruncMonth

        reservations_by_month = (
            all_reservations.annotate(month=TruncMonth("check_in"))
            .values("month")
            .annotate(
                total=Count("id"),
                pending=Count("id", filter=Q(status="pending")),
                confirmed=Count("id", filter=Q(status="confirmed")),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
            )
            .order_by("-month")
        )

        monthly_properties = []
        for item in reservations_by_month:
            month_label = (
                item["month"].strftime("%B %Y") if item["month"] else "Sin fecha"
            )

            month_reservations = (
                all_reservations.filter(
                    check_in__year=item["month"].year,
                    check_in__month=item["month"].month,
                )
                .values("property__title", "status")
                .order_by("property__title")
            )

            monthly_properties.append(
                {
                    "month": month_label,
                    "total": item["total"],
                    "pending": item["pending"],
                    "confirmed": item["confirmed"],
                    "completed": item["completed"],
                    "cancelled": item["cancelled"],
                    "reservations": list(month_reservations),
                }
            )

        context["monthly_properties"] = monthly_properties

        # ============================================
        # 3. Propiedades con más intenciones de reserva (HISTÓRICO TOTAL)
        # ============================================
        top_properties = (
            all_reservations.values("property__title")
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
        )
        context["top_properties"] = top_properties

        # ============================================
        # 4. Datos para gráfico (últimos 6 meses - TODAS)
        # ============================================
        six_months_ago = today - timedelta(days=180)
        chart_data = (
            all_reservations.filter(check_in__gte=six_months_ago)
            .annotate(month=TruncMonth("check_in"))
            .values("month")
            .annotate(
                total=Count("id"),
                pending=Count("id", filter=Q(status="pending")),
                confirmed=Count("id", filter=Q(status="confirmed")),
                completed=Count("id", filter=Q(status="completed")),
                cancelled=Count("id", filter=Q(status="cancelled")),
            )
            .order_by("month")
        )

        months = []
        pending_counts = []
        confirmed_counts = []
        completed_counts = []
        cancelled_counts = []
        for item in chart_data:
            if item["month"]:
                months.append(item["month"].strftime("%b %Y"))
                pending_counts.append(item["pending"])
                confirmed_counts.append(item["confirmed"])
                completed_counts.append(item["completed"])
                cancelled_counts.append(item["cancelled"])

        context["months"] = months
        context["pending_counts"] = pending_counts
        context["confirmed_counts"] = confirmed_counts
        context["completed_counts"] = completed_counts
        context["cancelled_counts"] = cancelled_counts

        # ============================================
        # 5. Últimas 10 reservas (TODAS)
        # ============================================
        recent_reservations = all_reservations.order_by("-created_at")[:10]
        context["recent_reservations"] = recent_reservations

        # ============================================
        # 6. Propiedades activas (para mantener)
        # ============================================
        total_properties = Property.objects.filter(is_active=True).count()
        context["total_properties"] = total_properties

        return context
