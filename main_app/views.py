from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Guitar, Pedal, Photo
from .forms import ServicingForm
import uuid
import boto3


# Create your views here.
class GuitarCreate(CreateView):
    model = Guitar
    fields = '__all__'

class GuitarUpdate(UpdateView):
    model = Guitar
    fields = '__all__'

class GuitarDelete(DeleteView):
    model = Guitar
    success_url = '/guitars/'

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def guitars_index(request):
    guitars = Guitar.objects.all()
    return render(request, 'guitars/index.html', { 'guitars': guitars })

def guitars_detail(request, guitar_id):
    guitar = Guitar.objects.get(id=guitar_id)
    servicing_form = ServicingForm()
    return render(request, 'guitars/detail.html', { 
        'guitar': guitar,
        'servicing_form': servicing_form 
    })


def add_service(request, guitar_id):
    form = ServicingForm(request.POST)
    if form.is_valid():
        new_service = form.save(commit=False)
        new_service.guitar_id = guitar_id
        new_service.save()
    return redirect('detail', guitar_id=guitar_id)

class PedalList(ListView):
    model = Pedal

class PedalDetail(DetailView):
    model = Pedal

class PedalCreate(CreateView):
    model = Pedal
    fields = '__all__'

class PedalUpdate(UpdateView):
    model = Pedal
    fields = '__all__'

class PedalDelete(DeleteView):
    model = Pedal
    success_url = '/pedals/'


