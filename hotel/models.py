# apps/core/models.py
from django.db import models

class Hotel(models.Model):
    """
    Modèle représentant l'hôtel lui-même
    """
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    
    def __str__(self):
        return self.name

class Configuration(models.Model):
    """
    Configuration générale de l'hôtel
    """
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE)
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='12:00')
    cancellation_policy = models.TextField()
    
    def __str__(self):
        return f"Configuration for {self.hotel.name}"