from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "customer",
        "vehicle",
        "pickup_date",
        "return_date",
        "status",
        "rating",
    )

    list_filter = (
        "status",
        "rating",
    )

    search_fields = (
        "customer__username",
        "vehicle__name",
    )