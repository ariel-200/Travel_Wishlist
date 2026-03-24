from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import PlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

# Create your views here.

@login_required()
def place_list(request):

    if request.method == 'POST':
        # create a new place
        form = PlaceForm(request.POST)
        place = form.save(commit=False) # creates a model object from the form
        place.user = request.user
        if form.is_valid(): # validation against DB constraints
            place.save() # saves place to DB
            return redirect('place_list') # reloads home page

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    place_form = PlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'place_form': place_form})


@login_required()
def places_visited(request):
    visited = Place.objects.filter(visited=True).order_by('name')
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})


@login_required()
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()

    return redirect('places_visited')


@login_required()
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)

    # Does this place belong to current user
    if place.user != request.user:
        return HttpResponseForbidden()

    # if POST request, validate for data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)

        return redirect('place_details', place_pk=place_pk)

    # if GET request, show Place info and form
    else:
        # if place is visited show form; if place not visited then no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_details.html', {'place': place, 'review_form': review_form})
        else:
            return render(request, 'travel_wishlist/place_details.html', {'place': place})


@login_required()
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


def about(request):
    author = 'Ariel'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
