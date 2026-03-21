import django_filters
from django import forms
from django.db.models import Q
from properties.models import Property, Category, Booking


class PropertyFilter(django_filters.FilterSet):
    # 1. Ubicación
    location = django_filters.ChoiceFilter(
        choices=Property.LOCATIONS, label="Ubicación"
    )

    # 2. Fechas
    check_in = django_filters.DateFilter(
        method="filter_available",
        label="Llegada",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    check_out = django_filters.DateFilter(
        method="filter_available",
        label="Salida",
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    # 3. Tipo de propiedad (Casa/Apartamento)
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), label="Tipo de propiedad", empty_label="Todos"
    )

    # 4. Tipo de alquiler (CORREGIDO: ahora es "room" en lugar de "apartment")
    rental_type = django_filters.ChoiceFilter(
        choices=Property.RENTAL_TYPES, label="Tipo de alquiler"
    )

    # 5. Habitaciones
    bedrooms = django_filters.NumberFilter(
        field_name="bedrooms",
        lookup_expr="exact",  # ✅ exacto, no gte
        label="Habitaciones",
    )

    # 6. Categoría de precio (NUEVO)
    price_category = django_filters.ChoiceFilter(
        choices=Property.PRICE_CATEGORIES,
        label="Categoría de precio",
        empty_label="Todos",
    )

    # Precio (filtro dinámico según categoría)
    price_min = django_filters.NumberFilter(
        method="filter_price", label="Precio mínimo (USD)"
    )

    price_max = django_filters.NumberFilter(
        method="filter_price", label="Precio máximo (USD)"
    )

    # 7. Huéspedes (NUEVO)
    guests = django_filters.NumberFilter(
        field_name="guests", lookup_expr="gte", label="Huéspedes (mínimo)"
    )

    # 8. Amenidades
    has_wifi = django_filters.BooleanFilter(label="WiFi")
    has_pool = django_filters.BooleanFilter(label="Piscina")
    has_parking = django_filters.BooleanFilter(label="Parqueo")
    has_ac = django_filters.BooleanFilter(label="Aire acondicionado")
    has_billiard = django_filters.BooleanFilter(label="Billar")
    has_washing_machine = django_filters.BooleanFilter(label="Lavadora")
    has_charcoal_oven = django_filters.BooleanFilter(label="Horno al carbón")

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

    def filter_price(self, queryset, name, value):
        """Filtra según la categoría de precio seleccionada"""
        price_category = self.data.get("price_category")

        if not price_category or not value:
            return queryset

        if price_category == "night":
            field = "price_per_night"
        elif price_category == "month":
            field = "price_per_month"
        else:
            return queryset

        if name == "price_min":
            return queryset.filter(**{f"{field}__gte": value})
        elif name == "price_max":
            return queryset.filter(**{f"{field}__lte": value})

        return queryset

    class Meta:
        model = Property
        fields = [
            "location",
            "check_in",
            "check_out",
            "category",
            "rental_type",
            "bedrooms",
            "price_category",
            "price_min",
            "price_max",
            "guests",
            "has_wifi",
            "has_pool",
            "has_parking",
            "has_ac",
            "has_billiard",
            "has_washing_machine",
            "has_charcoal_oven",
        ]
