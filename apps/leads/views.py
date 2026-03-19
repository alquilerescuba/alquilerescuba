from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.contrib.auth.mixins import UserPassesTestMixin
import json
from .models import Lead


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


class LeadListView(UserPassesTestMixin, ListView):
    model = Lead
    template_name = "leads/dashboard.html"
    context_object_name = "leads"
    paginate_by = 50

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Lead.objects.all().select_related("property")
