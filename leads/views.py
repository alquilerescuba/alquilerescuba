from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from leads.models import Lead


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
    template_name = "dashboard.html"  # ✅ Cambia a dashboard.html (sin leads/)
