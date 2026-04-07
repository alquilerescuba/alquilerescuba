from django.contrib import admin
from properties.models import Category, Property, PropertyImage, Booking, Review

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
        "price_category",
        "get_precio_display",
        "is_active",
    )
    list_filter = (
        "location",
        "category",
        "rental_type",
        "price_category",
        "is_active",
        "has_pool",
    )
    search_fields = ("title", "description", "address")
    inlines = [PropertyImageInline]

    fieldsets = (
        ("Información básica", {"fields": ("title", "description", "category", "is_active")}),
        ("Ubicación", {"fields": ("location", "address")}),
        ("Características", {"fields": ("bedrooms", "guests", "bathrooms", "rental_type")}),
        ("Amenidades", {
            "fields": (
                "has_wifi", "has_tv", "has_kitchen", "has_parking",
                "has_pool", "has_ac", "has_billiard", "has_washing_machine", "has_charcoal_oven",
            )
        }),
        ("Precios", {
            "fields": ("price_category", "price_per_night", "price_per_month", "price_per_daypass"),
            "description": "Selecciona la categoría de precio y completa el monto correspondiente.",
        }),
        ("Foto principal", {"fields": ("main_photo",)}),
    )

    def get_precio_display(self, obj):
        if obj.price_category == "night":
            return f"${obj.price_per_night} /noche"
        elif obj.price_category == "month":
            return f"${obj.price_per_month} /mes"
        return f"${obj.price_per_daypass} (Pasadía)"
    get_precio_display.short_description = "Precio"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("property", "guest_name", "start_date", "end_date", "created_at")
    list_filter = ("property", "start_date")
    search_fields = ("guest_name", "guest_email", "property__title")
    date_hierarchy = "start_date"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("property", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("property__title", "user__username", "comment")
