from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime

def validate_year(value):
    if value.year < 2015 or value.year > 2023:
        raise ValidationError(
            _('Year must be between 2015 and 2023'),
            params={'value': value},
        )

class CarMake(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    CONVERTIBLE = 'Convertible'
    PICKUP = 'Pickup'

    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (CONVERTIBLE, 'Convertible'),
        (PICKUP, 'Pickup'),
    ]

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    #dealer_id = models.IntegerField(blank=True,null=True)
    name = models.CharField(max_length=100)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    year = models.DateField(validators=[validate_year])
    engine = models.CharField(max_length=100, blank=True, null=True)
    horsepower = models.PositiveIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.name} ({self.car_make.name})'

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(year__year__gte=2015) & models.Q(year__year__lte=2023), name='year_range')
        ]