from django.db import models

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('Car', 'Car'),
        ('Bike', 'Bike'),
        ('Scooter', 'Scooter'),
        ('Van', 'Van'),
    ]

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    registration_number = models.CharField(max_length=20, unique=True)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    availability = models.BooleanField(default=True)
    description = models.TextField()
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model}"