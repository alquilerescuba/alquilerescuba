# properties/admin.py
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
        "title",
        "location",
        "price_category",
        "get_precio_display",
        "is_active",
        "thumbnail",
    )
    list_filter = ("location", "category", "rental_type", "price_category", "is_active")
    inlines = [PropertyImageInline]

    def thumbnail(self, obj):
        if obj.main_photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />',
                obj.main_photo.url,
            )
        return "No foto"

    def get_precio_display(self, obj):
        if obj.price_category == "night":
            return f"${obj.price_per_night} /noche"
        if obj.price_category == "month":
            return f"${obj.price_per_month} /mes"
        return f"${obj.price_per_daypass} (Pasadía)"

    get_precio_display.short_description = "Precio"


admin.site.register(Booking)
admin.site.register(Review)
