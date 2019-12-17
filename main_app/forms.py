from django.forms import ModelForm
from .models import Servicing

class ServicingForm(ModelForm):
  class Meta:
    model = Servicing
    fields = ['date', 'service']

