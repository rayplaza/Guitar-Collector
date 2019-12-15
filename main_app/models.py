from django.db import models

# Create your models here.
class Guitar(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    wood = models.CharField(max_length=100)
    pickup = models.CharField(max_length=100)
    description = models.TextField(max_length=250)


    
    
