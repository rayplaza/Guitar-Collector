from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Guitar, Pedal, Photo
from .forms import ServicingForm
import uuid
import boto3


# Create your views here.
class GuitarCreate(CreateView):
    model = Guitar
    fields = ['name', 'brand', 'model', 'year', 'wood', 'pickup', 'description']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GuitarUpdate(LoginRequiredMixin, UpdateView):
    model = Guitar
    fields = ['name', 'brand', 'model', 'year', 'wood', 'pickup', 'description']

class GuitarDelete(LoginRequiredMixin, DeleteView):
    model = Guitar
    success_url = '/guitars/'

def home(request):
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def guitars_index(request):
    guitars = Guitar.objects.filter(user=request.user)
    return render(request, 'guitars/index.html', { 'guitars': guitars })

@login_required
def guitars_detail(request, guitar_id):
    guitar = Guitar.objects.get(id=guitar_id)
    pedals_guitar_doesnt_have = Pedal.objects.exclude(id__in = guitar.pedals.all().values_list('id'))
    servicing_form = ServicingForm()
    return render(request, 'guitars/detail.html', {
      'guitar': guitar, 'servicing_form': servicing_form,
      'pedals': pedals_guitar_doesnt_have
    })

@login_required
def add_service(request, guitar_id):
    form = ServicingForm(request.POST)
    if form.is_valid():
        new_service = form.save(commit=False)
        new_service.guitar_id = guitar_id
        new_service.save()
    return redirect('detail', guitar_id=guitar_id)

@login_required
def assoc_pedal(request, guitar_id, pedal_id):
  Guitar.objects.get(id=guitar_id).pedals.add(pedal_id)
  return redirect('detail', guitar_id=guitar_id)


class PedalList(LoginRequiredMixin, ListView):
    model = Pedal

class PedalDetail(LoginRequiredMixin, DetailView):
    model = Pedal

class PedalCreate(LoginRequiredMixin, CreateView):
    model = Pedal
    fields = '__all__'

class PedalUpdate(LoginRequiredMixin, UpdateView):
    model = Pedal
    fields = '__all__'

class PedalDelete(LoginRequiredMixin, DeleteView):
    model = Pedal
    success_url = '/pedals/'

@login_required
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


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

