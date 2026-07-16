from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from bookings.models import Booking
from .forms import EditProfileForm


# Register
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {
        "form": form
    })


# Login
def user_login(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {
        "form": form
    })


# Logout
def user_logout(request):
    logout(request)
    return redirect("home")


# Profile
@login_required
def profile(request):

    total_bookings = Booking.objects.filter(
        customer=request.user
    ).count()

    pending = Booking.objects.filter(
        customer=request.user,
        status="Pending"
    ).count()

    completed = Booking.objects.filter(
        customer=request.user,
        status="Completed"
    ).count()

    cancelled = Booking.objects.filter(
        customer=request.user,
        status="Cancelled"
    ).count()

    return render(request, "profile.html", {

        "total_bookings": total_bookings,
        "pending": pending,
        "completed": completed,
        "cancelled": cancelled,

    })


# Edit Profile
@login_required
def edit_profile(request):

    if request.method == "POST":

        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:

        form = EditProfileForm(
            instance=request.user
        )

    return render(request, "edit_profile.html", {
        "form": form
    })