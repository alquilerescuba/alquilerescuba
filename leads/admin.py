from django.contrib import admin
from leads.models import Reservation, Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("property", "clicked_at", "is_processed", "commission_paid")
    list_filter = ("is_processed", "commission_paid", "clicked_at")
    search_fields = ("property__title", "notes")
    date_hierarchy = "clicked_at"


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "property",
        "status",
        "guest_name",
        "check_in",
        "check_out",
        "clicked_at",
        "commission_paid",
        "amount_paid",
    )
    list_filter = ("status", "commission_paid", "clicked_at", "property")
    search_fields = (
        "property__title",
        "property__id",
        "guest_name",
        "guest_email",
        "guest_phone",
        "notes",
    )
    readonly_fields = ("clicked_at", "ip_address", "status_updated_at")
    date_hierarchy = "clicked_at"
    ordering = ("-clicked_at",)

    fieldsets = (
        (
            "Propiedad y cliente",
            {
                "fields": (
                    "property",
                    "guest_name",
                    "guest_email",
                    "guest_phone",
                )
            },
        ),
        (
            "Fechas",
            {
                "fields": (
                    "check_in",
                    "check_out",
                )
            },
        ),
        (
            "Estado y seguimiento",
            {
                "fields": (
                    "status",
                    "status_updated_at",
                    "notes",
                )
            },
        ),
        (
            "Comisiones (solo administrador)",
            {
                "fields": (
                    "commission_paid",
                    "amount_paid",
                    "paid_at",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Datos de tracking",
            {
                "fields": (
                    "clicked_at",
                    "ip_address",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    # Permisos: solo superuser puede cambiar estado y comisiones
    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
