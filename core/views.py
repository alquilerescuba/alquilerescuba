from django.shortcuts import render
from properties.models import Property
from properties.filters import PropertyFilter


def home(request):
    # Obtenemos solo las activas
    queryset = Property.objects.filter(is_active=True)
    # Aplicamos el filtro
    property_filter = PropertyFilter(request.GET, queryset=queryset)

    context = {
        "filter": property_filter,
        "properties": property_filter.qs,
    }
    return render(request, "properties/list.html", context)
