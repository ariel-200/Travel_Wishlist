from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import PlaceForm

# Create your views here.
def place_list(request):

    if request.method == 'POST':
        # create a new place
        form = PlaceForm(request.POST)
        place = form.save() # creates a model object from the form
        if form.is_valid(): # validation against DB constraints
            place.save() # saves place to DB
            return redirect('place_list') # reloads home page

    places = Place.objects.filter(visited=False).order_by('name')
    place_form = PlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'place_form': place_form})


def places_visited(request):
    visited = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


def place_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()

    return redirect('places_visited')


def about(request):
    author = 'Ariel'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
