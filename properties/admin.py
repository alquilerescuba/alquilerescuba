from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Property, PropertyImage, Booking, Review
from leads.models import Reservation


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    readonly_fields = ("preview",)

    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto;" />', obj.image.url
            )
        return "Sin imagen"


class ReservationInline(admin.TabularInline):
    """Inline para ver/crear reservas desde la página de la propiedad"""

    model = Reservation
    extra = 1
    fields = (
        "check_in",
        "check_out",
        "guest_name",
        "guest_email",
        "guest_phone",
        "source",
        "status",
    )
    readonly_fields = ("clicked_at",)
    autocomplete_fields = ["property"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "title",
        "location",
        "precios_display",
        "is_active",
        "is_featured",
        "thumbnail",
    )
    list_display_links = ("id", "title")
    list_filter = (
        "location",
        "category",
        "rental_type",
        "is_active",
        "owner",
        "is_featured",
    )
    search_fields = (
        "id",
        "title",
        "description",
        "address",
    )
    inlines = [PropertyImageInline, ReservationInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "owner",
                    "title",
                    "description",
                    "category",
                    "location",
                    "address",
                )
            },
        ),
        (
            "Detalles",
            {
                "fields": (
                    "bedrooms",
                    "guests",
                    "bathrooms",
                    "rental_type",
                )
            },
        ),
        (
            "Precios",
            {
                "fields": (
                    "price_per_night",
                    "price_per_month",
                    "price_per_daypass",
                ),
                "description": "💡 Puedes llenar uno, dos o los tres precios. Si un campo queda vacío, no se mostrará.",
            },
        ),
        (
            "Amenidades",
            {
                "fields": (
                    "has_stable_electricity",
                    "has_pets_allowed",
                    "has_wifi",
                    "has_tv",
                    "has_kitchen",
                    "has_parking",
                    "has_pool",
                    "has_ac",
                    "has_billiard",
                    "has_washing_machine",
                    "has_charcoal_oven",
                )
            },
        ),
        (
            "Imagen",
            {
                "fields": ("main_photo",),
            },
        ),
        (
            "Estado",
            {
                "fields": ("is_active", "is_featured"),
            },
        ),
    )

    def precios_display(self, obj):
        precios = []
        if obj.price_per_night:
            precios.append(f"${obj.price_per_night}/noche")
        if obj.price_per_month:
            precios.append(f"${obj.price_per_month}/mes")
        if obj.price_per_daypass:
            precios.append(f"${obj.price_per_daypass}/pasadía")
        if not precios:
            return "Sin precio"
        return " · ".join(precios)

    precios_display.short_description = "Precios"

    def thumbnail(self, obj):
        if obj.main_photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />',
                obj.main_photo.url,
            )
        return "No foto"

    thumbnail.short_description = "Foto"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Admin de Booking (solo para consulta histórica)"""

    list_display = (
        "property",
        "start_date",
        "end_date",
        "guest_name",
        "created_at",
    )
    list_filter = ("property", "start_date", "end_date")
    search_fields = (
        "property__id",
        "property__title",
        "guest_name",
        "guest_email",
    )
    autocomplete_fields = ["property"]
    date_hierarchy = "start_date"
    ordering = ("-start_date",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.register(Review)
