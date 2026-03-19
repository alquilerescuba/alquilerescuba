import django_filters
from django import forms
from django.db.models import Q
from .models import Property, Category, Booking


class PropertyFilter(django_filters.FilterSet):
    # Filtros existentes
    location = django_filters.ChoiceFilter(
        choices=Property.LOCATIONS, label="Ubicación"
    )

    rental_type = django_filters.ChoiceFilter(
        choices=Property.RENTAL_TYPES, label="Tipo de alquiler"
    )

    bedrooms = django_filters.NumberFilter(
        field_name="bedrooms", lookup_expr="gte", label="Habitaciones (mínimo)"
    )

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), label="Tipo", empty_label="Todos"
    )

    # Filtros de precio
    price_per_night_min = django_filters.NumberFilter(
        field_name="price_per_night", lookup_expr="gte", label="Precio noche (mín)"
    )

    price_per_night_max = django_filters.NumberFilter(
        field_name="price_per_night", lookup_expr="lte", label="Precio noche (máx)"
    )

    # Amenidades
    has_wifi = django_filters.BooleanFilter(label="WiFi")
    has_pool = django_filters.BooleanFilter(label="Piscina")
    has_parking = django_filters.BooleanFilter(label="Parqueo")
    has_ac = django_filters.BooleanFilter(label="Aire acondicionado")

    # FILTROS DE FECHA CORREGIDOS
    check_in = django_filters.DateFilter(
        method="filter_available",
        label="Llegada",
        widget=forms.DateInput(attrs={"type": "date"}),  # ✅ CORREGIDO
    )

    check_out = django_filters.DateFilter(
        method="filter_available",
        label="Salida",
        widget=forms.DateInput(attrs={"type": "date"}),  # ✅ CORREGIDO
    )

    def filter_available(self, queryset, name, value):
        """Filtra propiedades disponibles en el rango de fechas"""
        check_in = self.data.get("check_in")
        check_out = self.data.get("check_out")

        if check_in and check_out:
            # Excluir propiedades con reservas que se solapan
            booked_properties = (
                Booking.objects.filter(
                    Q(start_date__lte=check_out) & Q(end_date__gte=check_in)
                )
                .values_list("property_id", flat=True)
                .distinct()
            )

            return queryset.exclude(id__in=booked_properties)

        return queryset

    class Meta:
        model = Property
        fields = ["location", "bedrooms", "rental_type", "category"]
