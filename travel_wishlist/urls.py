from django.urls import path
from . import views

urlpatterns = [
    path('', views.place_list, name='place_list'),
    path('visited', views.places_visited, name='places_visited'),
    path('about', views.about, name='about'),
    path('place/<int:place_pk>/was_visited', views.place_visited, name='place_visited'),
]