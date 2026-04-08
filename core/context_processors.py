from django.conf import settings


def global_settings(request):
    return {"BUSINESS_WHATSAPP": getattr(settings, "BUSINESS_WHATSAPP", "")}
