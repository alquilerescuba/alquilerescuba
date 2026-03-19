from django.contrib import admin
from .models import Category, Property, PropertyImage, Booking


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "slug")


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_location_display",
        "bedrooms",
        "rental_type",
        "price_per_night",
        "is_active",
    )
    list_filter = ("location", "category", "rental_type", "is_active", "has_pool")
    search_fields = ("title", "description", "address")
    inlines = [PropertyImageInline]

    fieldsets = (
        (
            "Información básica",
            {"fields": ("title", "description", "category", "is_active")},
        ),
        ("Ubicación", {"fields": ("location", "address")}),
        (
            "Características",
            {"fields": ("bedrooms", "guests", "bathrooms", "rental_type")},
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
                )
            },
        ),
        ("Precios", {"fields": ("price_per_night", "price_per_month")}),
        ("Foto principal", {"fields": ("main_photo",)}),
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("property", "start_date", "end_date", "guest_name", "created_at")
    list_filter = ("property", "start_date", "end_date")
    search_fields = ("guest_name", "guest_email", "property__title")
    date_hierarchy = "start_date"
