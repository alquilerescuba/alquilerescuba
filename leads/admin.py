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
        "source",
        "guest_name",
        "check_in",
        "check_out",
        "clicked_at",
        "commission_paid",
        "amount_paid",
    )
    list_filter = ("status", "source", "commission_paid", "clicked_at", "property")
    search_fields = (
        "property__title",
        "property__id",
        "guest_name",
        "guest_email",
        "guest_phone",
        "notes",
    )
    autocomplete_fields = ["property"]
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
                    "source",
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

    def has_change_permission(self, request, obj=None):
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            # El staff puede editar todo EXCEPTO comisiones
            return ["commission_paid", "amount_paid", "paid_at"]
        return self.readonly_fields
