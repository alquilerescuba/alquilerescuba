from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta
import json
from .models import Lead
from properties.models import Property


@require_POST
@csrf_exempt
def track_lead(request):
    try:
        data = json.loads(request.body)
        property_id = data.get("property_id")

        if property_id:
            Lead.objects.create(
                property_id=property_id, ip_address=request.META.get("REMOTE_ADDR")
            )
            return JsonResponse({"status": "ok"})
    except:
        pass

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

        # ============================================
        # 1. Resumen general
        # ============================================
        total_properties = Property.objects.filter(is_active=True).count()
        total_leads = Lead.objects.count()
        leads_concretados = Lead.objects.filter(commission_paid=True).count()

        conversion_rate = 0
        if total_leads > 0:
            conversion_rate = round((leads_concretados / total_leads) * 100, 1)

        context["total_properties"] = total_properties
        context["total_leads"] = total_leads
        context["leads_concretados"] = leads_concretados
        context["conversion_rate"] = conversion_rate

        # Leads de hoy
        today = timezone.now().date()
        leads_today = Lead.objects.filter(clicked_at__date=today).count()
        context["leads_today"] = leads_today

        # ============================================
        # 2. Total de propiedades por ubicación
        # ============================================
        properties_by_location = (
            Property.objects.filter(is_active=True)
            .values("location")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        # Mapeo de códigos de ubicación a nombres legibles
        location_names = dict(Property.LOCATIONS)
        for item in properties_by_location:
            item["location_name"] = location_names.get(
                item["location"], item["location"]
            )

        context["properties_by_location"] = properties_by_location

        # ============================================
        # 3. Total de leads por ubicación
        # ============================================
        leads_by_location = (
            Lead.objects.values("property__location")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        for item in leads_by_location:
            item["location_name"] = location_names.get(
                item["property__location"], item["property__location"]
            )

        context["leads_by_location"] = leads_by_location

        # ============================================
        # 4. Top 5 propiedades con más leads
        # ============================================
        top_properties = (
            Lead.objects.values("property__title", "property__location")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )

        for item in top_properties:
            item["location_name"] = location_names.get(
                item["property__location"], item["property__location"]
            )

        context["top_properties"] = top_properties

        # ============================================
        # 5. Leads por mes (últimos 6 meses)
        # ============================================
        six_months_ago = timezone.now() - timedelta(days=180)
        leads_by_month = (
            Lead.objects.filter(clicked_at__gte=six_months_ago)
            .annotate(month=TruncMonth("clicked_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("month")
        )

        months = []
        leads_counts = []
        for item in leads_by_month:
            if item["month"]:
                months.append(item["month"].strftime("%b %Y"))
                leads_counts.append(item["total"])

        context["months"] = months
        context["leads_counts"] = leads_counts

        # ============================================
        # 6. Últimos 10 leads
        # ============================================
        recent_leads = Lead.objects.all().order_by("-clicked_at")[:10]
        context["recent_leads"] = recent_leads

        return context
