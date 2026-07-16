from django.urls import path
from . import views

urlpatterns = [

    # Home
    path(
        "home/",
        views.home,
        name="home"
    ),

    # Vehicle List
    path(
        "",
        views.vehicle_list,
        name="vehicle_list"
    ),

    path(
        "vehicles/",
        views.vehicle_list,
        name="vehicle_list"
    ),

    # Vehicle Details
    path(
        "vehicles/<int:pk>/",
        views.vehicle_detail,
        name="vehicle_detail"
    ),

    # About
    path(
        "about/",
        views.about,
        name="about"
    ),

    # Contact
    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    # Admin Dashboard
    path(
        "dashboard/admin/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Revenue Report
    path(
        "dashboard/revenue/",
        views.revenue_report,
        name="revenue_report"
    ),

]