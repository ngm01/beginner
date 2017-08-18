from __future__ import unicode_literals

from django.db import models
from ..loginreg.models import User
import datetime

# Create your models here.
class tripManager(models.Manager):
	def validateTrip(self, postData):
		errors = {}
		flag = True
		today = datetime.datetime.today()
		if not self.validateDate(postData['trip_start']) or not self.validateDate(postData['trip_end']):
			errors['date'] = "Please enter dates in MM/DD/YYYY format."
			flag = False
		if self.validateDate(postData['trip_start']):
			if self.validateDate(postData['trip_start']) < today:
				errors['bad_start'] = "Start date cannot be in the past."
				flag = False
		if self.validateDate(postData['trip_end']):
			if self.validateDate(postData['trip_end']) < self.validateDate(postData['trip_start']):
				errors['bad_end'] = "End date must be in the future."
				flag = False
		if not postData['destination']:
			errors['destination'] = "Destination field cannot be blank."
			flag = False
		if not postData['description']:
			errors['description'] = "Description field cannot be blank."
			flag = False

		if flag:
			new_trip = Trip.objects.create(destination=postData['destination'], 
				description=postData['description'],
				trip_start = self.validateDate(postData['trip_start']),
				trip_end = self.validateDate(postData['trip_end']),
				trip_creator = User.objects.get(id=postData['user']))
			new_trip.travelers.add(User.objects.get(id=postData['user']))
			return (True, new_trip)
		else:
			return (False, errors)


	def validateDate(self, dt):
		try:
			valid_date = datetime.datetime.strptime(dt, '%m/%d/%Y')
			return valid_date
		except ValueError:
			return False



class Trip(models.Model):
	destination = models.CharField(max_length=255)
	description = models.TextField()
	trip_start = models.DateTimeField()
	trip_end = models.DateTimeField()

	# here we need to create relationships with the Users class from the loginreg app:

	# a one-to-many relationship between trip_creator and trips
	trip_creator = models.ForeignKey(User)

	# a many-to-many relationship between trips and users
	travelers = models.ManyToManyField(User, related_name="trips_travelers")

	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

	objects = tripManager()
