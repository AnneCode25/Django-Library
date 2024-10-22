from django.urls import path
from . import views

urlpatterns = [
    path('available-media/', views.available_media, name='available_media'),
]