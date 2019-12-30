from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


SERVICES = (
    ('S', 'Strings'),
    ('T', 'Tuning'),
    ('A', 'Adjustment'),
    ('C', 'Cleaning')
)


class Pedal(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    pedalType = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pedals_detail', kwargs={'pk': self.id})

# Create your models here.
class Guitar(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    wood = models.CharField(max_length=100)
    pickup = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'guitar_id': self.id})

class Servicing(models.Model):
    date = models.DateField('service date')
    service = models.CharField(
        max_length=1,
        choices=SERVICES,
        default=SERVICES[0][0]
        )

    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_service_display()} on {self.date}"

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    guitar = models.ForeignKey(Guitar, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for guitar_id: {self.guitar_id} @{self.url}"









    




    
    
