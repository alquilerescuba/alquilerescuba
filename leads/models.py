from django.db import models
from properties.models import Property


class Lead(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name="Propiedad"
    )
    clicked_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de contacto"
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")

    is_processed = models.BooleanField(default=False, verbose_name="Gestionado")
    commission_paid = models.BooleanField(default=False, verbose_name="Comisión pagada")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de pago")
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto pagado",
    )
    notes = models.TextField(blank=True, verbose_name="Notas")

    class Meta:
        app_label = "leads"
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"Lead: {self.property.title} - {self.clicked_at.strftime('%d/%m/%Y')}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pendiente"),
        ("confirmed", "Confirmada"),
        ("completed", "Completada"),
        ("cancelled", "Cancelada"),
    ]

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, verbose_name="Propiedad"
    )

    # Datos del cliente (opcionales al inicio)
    guest_name = models.CharField(
        max_length=100, blank=True, verbose_name="Nombre del huésped"
    )
    guest_email = models.EmailField(blank=True, verbose_name="Email del huésped")
    guest_phone = models.CharField(
        max_length=20, blank=True, verbose_name="Teléfono del huésped"
    )

    # Fechas
    check_in = models.DateField(null=True, blank=True, verbose_name="Fecha de llegada")
    check_out = models.DateField(null=True, blank=True, verbose_name="Fecha de salida")

    # Estado
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Estado"
    )

    # Tracking (ex-Lead)
    clicked_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de contacto"
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP")

    # Comisiones (solo tú lo editas)
    commission_paid = models.BooleanField(default=False, verbose_name="Comisión pagada")
    amount_paid = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto pagado (USD)",
    )
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de pago")

    # Notas
    notes = models.TextField(blank=True, verbose_name="Notas")

    # Control de cambios de estado
    status_updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Última actualización de estado"
    )

    class Meta:
        app_label = "leads"
        verbose_name = "Reserva"
        verbose_name_plural = "Reservas"
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"Reserva #{self.id} - {self.property.title}"
