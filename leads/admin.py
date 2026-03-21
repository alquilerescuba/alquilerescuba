from django.contrib import admin
from leads.models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("property", "clicked_at", "is_processed", "commission_paid")
    list_filter = ("is_processed", "commission_paid", "clicked_at")
    search_fields = ("property__title", "notes")
    date_hierarchy = "clicked_at"
