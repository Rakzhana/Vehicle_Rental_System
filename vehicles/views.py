from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Q, Avg, Count
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Vehicle
from bookings.models import Booking


# ----------------------------
# Home Page
# ----------------------------
def home(request):
    return render(request, "home.html")


# ----------------------------
# Vehicle List
# Search + Filter + Ratings
# ----------------------------
def vehicle_list(request):

    vehicles = Vehicle.objects.all()

    # Search
    query = request.GET.get("q")

    if query:
        vehicles = vehicles.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(vehicle_type__icontains=query)
        )

    # Filter by vehicle type
    vehicle_type = request.GET.get("type")

    if vehicle_type:
        vehicles = vehicles.filter(
            vehicle_type__iexact=vehicle_type
        )

    # Average Rating and Review Count
    vehicles = vehicles.annotate(
        avg_rating=Avg("booking__rating"),
        review_count=Count("booking__rating")
    )

    return render(
        request,
        "vehicle_list.html",
        {
            "vehicles": vehicles
        }
    )


# ----------------------------
# Vehicle Detail
# ----------------------------
def vehicle_detail(request, pk):

    vehicle = get_object_or_404(
        Vehicle,
        pk=pk
    )

    reviews = Booking.objects.filter(
        vehicle=vehicle,
        rating__isnull=False
    ).exclude(
        review=""
    )

    avg_rating = reviews.aggregate(
        Avg("rating")
    )["rating__avg"]

    return render(
        request,
        "vehicle_detail.html",
        {
            "vehicle": vehicle,
            "reviews": reviews,
            "avg_rating": avg_rating,
        }
    )


# ----------------------------
# About Page
# ----------------------------
def about(request):
    return render(request, "about.html")


# ----------------------------
# Contact Page
# ----------------------------
def contact(request):
    return render(request, "contact.html")


# ----------------------------
# Admin Dashboard
# ----------------------------
@staff_member_required
def admin_dashboard(request):

    total_vehicles = Vehicle.objects.count()

    available_vehicles = Vehicle.objects.filter(
        availability=True
    ).count()

    total_bookings = Booking.objects.count()

    pending = Booking.objects.filter(
        status="Pending"
    ).count()

    approved = Booking.objects.filter(
        status="Approved"
    ).count()

    completed = Booking.objects.filter(
        status="Completed"
    ).count()

    cancelled = Booking.objects.filter(
        status="Cancelled"
    ).count()

    total_users = User.objects.count()

    total_revenue = sum(
        booking.total_amount
        for booking in Booking.objects.filter(
            status="Completed"
        )
    )

    context = {

        # Dashboard Cards

        "total_vehicles": total_vehicles,

        "available_vehicles": available_vehicles,

        "total_bookings": total_bookings,

        "pending": pending,

        "approved": approved,

        "completed": completed,

        "cancelled": cancelled,

        "total_users": total_users,

        "total_revenue": total_revenue,

        # Chart Data

        "chart_pending": pending,

        "chart_approved": approved,

        "chart_completed": completed,

        "chart_cancelled": cancelled,

    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )
# ----------------------------
# Revenue Report
# ----------------------------
@staff_member_required
def revenue_report(request):

    today = timezone.now().date()

    month = today.month
    year = today.year

    completed_bookings = Booking.objects.filter(
        status="Completed"
    )

    # Total Revenue
    total_revenue = completed_bookings.aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # Today's Revenue
    today_revenue = completed_bookings.filter(
        pickup_date=today
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # Monthly Revenue
    monthly_revenue = completed_bookings.filter(
        pickup_date__month=month,
        pickup_date__year=year
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # Yearly Revenue
    yearly_revenue = completed_bookings.filter(
        pickup_date__year=year
    ).aggregate(
        total=Sum("total_amount")
    )["total"] or 0

    # Last 7 Days Revenue
    labels = []
    data = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        revenue = completed_bookings.filter(
            pickup_date=day
        ).aggregate(
            total=Sum("total_amount")
        )["total"] or 0

        labels.append(day.strftime("%d %b"))
        data.append(float(revenue))

    context = {

        "today_revenue": today_revenue,
        "monthly_revenue": monthly_revenue,
        "yearly_revenue": yearly_revenue,
        "total_revenue": total_revenue,

        "labels": labels,
        "data": data,

    }

    return render(
        request,
        "revenue_report.html",
        context
    )