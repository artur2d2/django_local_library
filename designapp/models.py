from django.db import models

# Create your models here.

class values_data(models.Model):
    liquid_flux = models.DecimalField(max_digits=30, decimal_places=6)
    vapor_flux = models.DecimalField(max_digits=30, decimal_places=6)
    liquid_density = models.DecimalField(max_digits=30, decimal_places=6)
    vapor_density = models.DecimalField(max_digits=30, decimal_places=6)
    API = models.DecimalField(max_digits=30, decimal_places=6)
