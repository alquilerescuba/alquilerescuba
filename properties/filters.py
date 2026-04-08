import django_filters
from django import forms
from .models import Property, Category


class PropertyFilter(django_filters.FilterSet):
    location = django_filters.ChoiceFilter(
        choices=Property.LOCATIONS, label="Ubicación"
    )
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(), empty_label="Todos"
    )
    price_category = django_filters.ChoiceFilter(
        choices=Property.PRICE_CATEGORIES, empty_label="Todos"
    )

    price_min = django_filters.NumberFilter(method="filter_price")
    price_max = django_filters.NumberFilter(method="filter_price")

    def filter_price(self, queryset, name, value):
        cat = self.data.get("price_category")
        if not cat or value is None:
            return queryset

        mapping = {
            "night": "price_per_night",
            "month": "price_per_month",
            "daypass": "price_per_daypass",
        }
        field = mapping.get(cat)
        if not field:
            return queryset

        lookup = "gte" if name == "price_min" else "lte"
        return queryset.filter(**{f"{field}__{lookup}": value})

    class Meta:
        model = Property
        fields = ["location", "category", "price_category"]
