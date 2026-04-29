from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Property, PropertyImage, Booking, Review


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",  # 👈 AÑADIDO: muestra el ID de la propiedad
        "title",
        "location",
        "precios_display",
        "is_active",
        "thumbnail",
    )
    list_display_links = ("id", "title")  # 👈 AÑADIDO: el ID también es un enlace
    list_filter = ("location", "category", "rental_type", "is_active")
    search_fields = (
        "id",
        "title",
        "description",
        "address",
    )  # 👈 MODIFICADO: añadido 'id'
    inlines = [PropertyImageInline]

    fieldsets = (
        (
            None,
            {
                "fields": (
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
                "fields": ("is_active",),
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


admin.site.register(Booking)
admin.site.register(Review)
