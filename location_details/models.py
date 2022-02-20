from django.db import models


class LocationDetails(models.Model):
    """
    The class represents a location model which contain some details about the location such as location name, coordinates
    details, small description about the location, and its state and population
    """
    name = models.CharField(max_length=250)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField()
    state = models.CharField(max_length=300)
    population = models.PositiveBigIntegerField()
