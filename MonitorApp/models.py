from django.db import models

# Create your models here.

#Here Goes the OBJ used in the DISPLAY pages
class EnvironmentData(models.Model):
    temperature = models.CharField(max_length=50)
    humidity = models.CharField(max_length=50)
    pressure = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
