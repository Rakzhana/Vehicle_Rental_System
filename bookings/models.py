from django.db import models
from django.contrib.auth.models import User
from vehicles.models import Vehicle

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Approved', 'Approved'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]


class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    return_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    rating = models.PositiveIntegerField(
    null=True,
    blank=True
)

    review = models.TextField(
    blank=True
)

    def __str__(self):
        return f"{self.customer.username} - {self.vehicle.name}"