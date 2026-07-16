from django.urls import path
from . import views

urlpatterns = [

    # Book Vehicle
    path(
        "book/<int:pk>/",
        views.book_vehicle,
        name="book_vehicle"
    ),

    # My Bookings
    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings"
    ),

    # Payment
    path(
        "payment/<int:pk>/",
        views.payment,
        name="payment"
    ),

    path(
        "payment-success/<int:pk>/",
        views.payment_success,
        name="payment_success"
    ),

    # Cancel Booking (User)
    path(
        "cancel/<int:pk>/",
        views.cancel_booking,
        name="cancel_booking"
    ),

    # Receipt
    path(
        "receipt/<int:pk>/",
        views.booking_receipt,
        name="booking_receipt"
    ),

    # Download Receipt PDF
    path(
        "receipt/<int:pk>/pdf/",
        views.download_receipt_pdf,
        name="download_receipt_pdf"
    ),

    # Review
    path(
        "review/<int:pk>/",
        views.review_booking,
        name="review_booking"
    ),

    # -----------------------------
    # ADMIN BOOKING MANAGEMENT
    # -----------------------------

    path(
        "admin-bookings/",
        views.admin_bookings,
        name="admin_bookings"
    ),

    path(
        "approve/<int:pk>/",
        views.approve_booking,
        name="approve_booking"
    ),

    path(
        "complete/<int:pk>/",
        views.complete_booking,
        name="complete_booking"
    ),

    path(
        "admin-cancel/<int:pk>/",
        views.cancel_booking_admin,
        name="cancel_booking_admin"
    ),

]