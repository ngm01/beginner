from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import datetime

# Create your views here.
def index(request):
	context = {'user': User.objects.get(id=request.session['logged_in']),
	'mytrips': User.objects.get(id=request.session['logged_in']).trips_travelers.all(),
	'alltrips': Trip.objects.exclude(trip_creator=request.session['logged_in'])}
	return render(request, 'travels/index.html', context)

def destinations(request, id):
	context = {'trip': Trip.objects.get(id=id),
	'user': User.objects.get(id=request.session['logged_in'])
	}

	return render(request, 'travels/destinations.html', context)

def add(request):
	return render(request, 'travels/add.html')

def join(request):
	Trip.objects.get(id=request.POST['trip']).travelers.add(User.objects.get(id=request.POST['user']))
	messages.success(request, "You have successfully join this trip!")
	return redirect('/')

def newtrip(request):
	make_trip =  Trip.objects.validateTrip(request.POST)
	if make_trip[0] == True:
		return redirect('/')
	else:
		for k,v in make_trip[1].iteritems():
 			messages.error(request, v, extra_tags=k)
 	return redirect('/travels/add')

def logout(request):
	request.session.flush()
	return redirect('/')