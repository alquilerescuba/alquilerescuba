from django.db import migrations
from django.db import models


def migrate_leads_and_bookings_to_reservations(apps, schema_editor):
    Lead = apps.get_model("leads", "Lead")
    Booking = apps.get_model("properties", "Booking")
    Reservation = apps.get_model("leads", "Reservation")

    # Migrar Leads
    for lead in Lead.objects.all():
        # Determinar estado según los campos existentes
        if lead.commission_paid:
            status = "completed"
        elif lead.is_processed:
            status = "confirmed"
        else:
            status = "pending"

        Reservation.objects.create(
            property=lead.property,
            clicked_at=lead.clicked_at,
            ip_address=lead.ip_address,
            commission_paid=lead.commission_paid,
            amount_paid=lead.amount_paid,
            paid_at=lead.paid_at,
            notes=lead.notes,
            status=status,
            # Los campos de Booking se dejan vacíos (no tenemos datos en Lead)
        )

    # Migrar Bookings
    for booking in Booking.objects.all():
        # Verificar si ya existe una reserva para este booking
        # (asumimos que es completada)
        Reservation.objects.create(
            property=booking.property,
            guest_name=booking.guest_name,
            guest_email=booking.guest_email,
            guest_phone=booking.guest_phone,
            check_in=booking.start_date,
            check_out=booking.end_date,
            clicked_at=booking.created_at,
            status="completed",
            commission_paid=False,  # Por defecto, no pagado
            notes=f"Migrado desde Booking #{booking.id}",
        )


def reverse_migration(apps, schema_editor):
    # No se puede revertir fácilmente, se deja vacío
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("leads", "0001_initial"),  # Ajusta según tu última migración de leads
        (
            "properties",
            "0001_initial",
        ),  # Ajusta según tu última migración de properties
    ]

    operations = [
        migrations.RunPython(
            migrate_leads_and_bookings_to_reservations, reverse_migration
        ),
    ]
