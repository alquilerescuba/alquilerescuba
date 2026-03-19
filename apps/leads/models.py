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
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-clicked_at"]

    def __str__(self):
        return f"Lead: {self.property.title} - {self.clicked_at.strftime('%d/%m/%Y')}"
