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


def add_photo(request, guitar_id):
  S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
  BUCKET = 'catcollector-rpc'
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
        s3.upload_fileobj(photo_file, BUCKET, key)
        url = f'{S3_BASE_URL}{BUCKET}/{key}'
        photo = Photo(url=url, guitar_id=guitar_id)
        photo.save()
      except:
        print('An error occurrrrrred uploading file to S3')
  return redirect('detail', guitar_id=guitar_id)

