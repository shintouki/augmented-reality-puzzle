from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
import json

from .models import Location

def index(request):
    """Homepage view"""
    context = {'text': 'Welcome to our game'}
    return render(request, 'game/index.html', context)

# This isn't used right now
# def register(request):
#     context = {'text': 'Register here'}
#     return render(request, 'registration/register.html', context)

def users(request):
    """User list view"""
    context = {'text': 'User list here'}
    return render(request, 'game/users.html', context)

def user_detail(request, user_id):
    """User profile view"""
    return HttpResponse("This page will have user details")

def leaderboard(request):
    """Leaderboard view"""
    context = {'text': 'Leaderboard goes here'}
    return render(request, 'game/leaderboard.html', context)

def play(request):
    """Game view"""
    # context = {'text': 'Leaderboard goes here'}
    return render(request, 'game/play.html')

def infection_rates(request):
    location_list = Location.objects.all()
    locationJSON = serializers.serialize('json', location_list)
    # Convert JSON to python dict
    locationObject = json.loads(locationJSON)

    # Create a new object and make the keys be the location names so it's easier to search later
    outputObject = {}
    for location in locationObject:
        location_text = location['fields']['location_text']
        outputObject[location_text] = location
        return HttpResponse(json.dumps(outputObject), content_type='application/javascript')

def win(request, location_name):
    """Saving matches won to database"""
    location = get_object_or_404(Location, location_text=location_name)
    location.matches_won += 1
    location.save()
    return HttpResponse("success")

def lose(request, location_name):
    """Saving matches lost to database"""
    location = get_object_or_404(Location, location_text=location_name)
    location.matches_lost += 1
    location.save()
    return HttpResponse("success")
    
