from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Booking
from .forms import BookingForm, ReviewForm
from vehicles.models import Vehicle
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# -----------------------------
# Book Vehicle
# -----------------------------
@login_required
def book_vehicle(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            booking = form.save(commit=False)

            booking.customer = request.user
            booking.vehicle = vehicle

            # Validate dates
            if booking.return_date <= booking.pickup_date:
                form.add_error(
                    "return_date",
                    "Return date must be after pickup date."
                )

                return render(request, "book_vehicle.html", {
                    "form": form,
                    "vehicle": vehicle
                })

            # Check for overlapping bookings
            existing_booking = Booking.objects.filter(
                vehicle=vehicle,
                status__in=["Pending", "Approved", "Completed"],
                pickup_date__lte=booking.return_date,
                return_date__gte=booking.pickup_date
            ).exists()

            if existing_booking:
                form.add_error(
                    None,
                    "This vehicle is already booked for the selected dates."
                )

                return render(request, "book_vehicle.html", {
                    "form": form,
                    "vehicle": vehicle
                })

            # Calculate rental amount
            days = (booking.return_date - booking.pickup_date).days

            booking.total_amount = days * vehicle.price_per_day

            booking.save()

            return redirect("payment", pk=booking.pk)

    else:
        form = BookingForm()

    return render(request, "book_vehicle.html", {
        "form": form,
        "vehicle": vehicle
    })


# -----------------------------
# My Bookings
# -----------------------------
@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        customer=request.user
    ).order_by("-id")

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })


# -----------------------------
# Payment
# -----------------------------
@login_required
def payment(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    if request.method == "POST":

        booking.status = "Approved"
        booking.save()

        messages.success(
            request,
            "Payment completed successfully."
        )

        return redirect(
            "payment_success",
            pk=booking.pk
        )

    return render(request, "payment.html", {
        "booking": booking
    })


# -----------------------------
# Payment Success
# -----------------------------
@login_required
def payment_success(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    return render(request, "payment_success.html", {
        "booking": booking
    })


# -----------------------------
# Cancel Booking
# -----------------------------
@login_required
def cancel_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    if booking.status in ["Pending", "Approved"]:

        booking.status = "Cancelled"
        booking.save()

        messages.success(
            request,
            "Booking cancelled successfully."
        )

    else:

        messages.error(
            request,
            "This booking cannot be cancelled."
        )

    return redirect("my_bookings")


# -----------------------------
# Booking Receipt
# -----------------------------
@login_required
def booking_receipt(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    days = (
        booking.return_date -
        booking.pickup_date
    ).days

    return render(request, "booking_receipt.html", {
        "booking": booking,
        "days": days
    })

@login_required
def download_receipt_pdf(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    response = HttpResponse(content_type="application/pdf")

    response["Content-Disposition"] = (
        f'attachment; filename="Booking_{booking.pk}.pdf"'
    )

    pdf = canvas.Canvas(response)

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(180, 800, "Vehicle Rental System")

    pdf.setFont("Helvetica", 14)
    pdf.drawString(220, 775, "Booking Receipt")

    y = 730

    pdf.drawString(60, y, f"Booking ID : {booking.pk}")
    y -= 30

    pdf.drawString(60, y, f"Customer : {booking.customer.username}")
    y -= 30

    pdf.drawString(
        60,
        y,
        f"Vehicle : {booking.vehicle.brand} {booking.vehicle.model}"
    )
    y -= 30

    pdf.drawString(
        60,
        y,
        f"Pickup Date : {booking.pickup_date}"
    )
    y -= 30

    pdf.drawString(
        60,
        y,
        f"Return Date : {booking.return_date}"
    )
    y -= 30

    days = (booking.return_date - booking.pickup_date).days

    pdf.drawString(
        60,
        y,
        f"Rental Days : {days}"
    )
    y -= 30

    pdf.drawString(
        60,
        y,
        f"Total Amount : ₹{booking.total_amount}"
    )
    y -= 30

    pdf.drawString(
        60,
        y,
        f"Status : {booking.status}"
    )

    y -= 60

    pdf.setFont("Helvetica-Bold", 12)

    pdf.drawString(
        60,
        y,
        "Thank you for choosing Vehicle Rental System!"
    )

    pdf.save()

    return response
# -----------------------------
# Review Booking
# -----------------------------
@login_required
def review_booking(request, pk):

    booking = get_object_or_404(
        Booking,
        pk=pk,
        customer=request.user
    )

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=booking
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Thank you for your review!"
            )

            return redirect("my_bookings")

    else:

        form = ReviewForm(instance=booking)

    return render(request, "review_booking.html", {
        "form": form,
        "booking": booking,
    })
@staff_member_required
def admin_bookings(request):

    bookings = Booking.objects.select_related(
        "customer",
        "vehicle"
    ).order_by("-id")

    search = request.GET.get("search")

    status = request.GET.get("status")

    if search:
        bookings = bookings.filter(
            Q(customer__username__icontains=search) |
            Q(vehicle__brand__icontains=search) |
            Q(vehicle__model__icontains=search)
        )

    if status:
        bookings = bookings.filter(status=status)

    return render(request, "admin_bookings.html", {
        "bookings": bookings
    })


@staff_member_required
def approve_booking(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    booking.status = "Approved"
    booking.save()

    messages.success(request, "Booking approved successfully.")

    return redirect("admin_bookings")


@staff_member_required
def complete_booking(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    booking.status = "Completed"
    booking.save()

    messages.success(request, "Booking marked as completed.")

    return redirect("admin_bookings")


@staff_member_required
def cancel_booking_admin(request, pk):

    booking = get_object_or_404(Booking, pk=pk)

    booking.status = "Cancelled"
    booking.save()

    messages.success(request, "Booking cancelled.")

    return redirect("admin_bookings")