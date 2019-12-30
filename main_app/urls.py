from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('guitars/', views.guitars_index, name='index'),
    path('guitars/<int:guitar_id>/', views.guitars_detail, name='detail'),
    path('guitars/create/', views.GuitarCreate.as_view(), name='guitars_create'),
    path('guitars/<int:pk>/update/', views.GuitarUpdate.as_view(), name='guitars_update'),
    path('guitars/<int:pk>/delete/', views.GuitarDelete.as_view(), name='guitars_delete'),
    path('guitars/<int:guitar_id>/add_service/', views.add_service, name='add_service'),
    path('guitars/<int:guitar_id>/assoc_pedal/<int:pedal_id>/', views.assoc_pedal, name='assoc_pedal'),
    path('guitars/<int:guitar_id>/add_photo/', views.add_photo, name='add_photo'),
    path('pedals/', views.PedalList.as_view(), name='pedals_index'),
    path('pedals/<int:pk>/', views.PedalDetail.as_view(), name='pedals_detail'),
    path('pedals/create/', views.PedalCreate.as_view(), name='pedals_create'),
    path('pedals/<int:pk>/update/', views.PedalUpdate.as_view(), name='pedals_update'),
    path('pedals/<int:pk>/delete/', views.PedalDelete.as_view(), name='pedals_delete'),
    path('accounts/signup/', views.signup, name='signup'),
]