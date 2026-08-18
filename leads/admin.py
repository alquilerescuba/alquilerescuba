from django.contrib import admin
from django.utils.html import format_html
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
        "get_status_display",
        "guest_name",
        "check_in",
        "check_out",
        "clicked_at",
        "commission_paid_display",
        "amount_paid_display",
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

    def get_status_display(self, obj):
        colors = {
            "pending": "warning",
            "confirmed": "info",
            "completed": "success",
            "cancelled": "danger",
        }
        labels = {
            "pending": "Pendiente",
            "confirmed": "Confirmada",
            "completed": "Completada",
            "cancelled": "Cancelada",
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.status, "secondary"),
            labels.get(obj.status, obj.status),
        )

    get_status_display.short_description = "Estado"

    def commission_paid_display(self, obj):
        if obj.commission_paid:
            return format_html('<span class="badge bg-success">✅ Pagada</span>')
        return format_html('<span class="badge bg-secondary">⏳ Pendiente</span>')

    commission_paid_display.short_description = "Comisión"

    def amount_paid_display(self, obj):
        if obj.amount_paid:
            return f"${obj.amount_paid:.2f}"
        return "-"

    amount_paid_display.short_description = "Monto"

    # Permisos: solo superuser puede cambiar estado y comisiones
    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser:
            # Usuario normal solo puede ver, no editar
            return False
        return super().has_change_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            # Usuario normal no puede editar nada
            return [f.name for f in self.model._meta.fields]
        return self.readonly_fields
