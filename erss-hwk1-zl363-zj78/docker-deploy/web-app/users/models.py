from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta

# Create your models here.

VEHICLE_TYPES = [
    ('Sedan', 'Sedan'),
    ('Coupe', 'Coupe'),
    ('Sports Car', 'Sports Car'),
    ('Hatchback', 'Hatchback'),
    ('Station Wagon', 'Station Wagon'),
    ('SUV', 'SUV'),
]

class User(models.Model):
    username = models.CharField(max_length = 50, primary_key = True)
    password = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    email = models.EmailField(default = '@example.com', blank = False)

    def __str__(self):
        return self.name
    

class RideOwner(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    dest_addr = models.CharField(max_length = 150)
    arrival = models.DateTimeField(default = datetime.now)
    num_passenger = models.PositiveSmallIntegerField(default = 1, validators=[MinValueValidator(1)])
    vehicle_type = models.CharField(max_length = 15, choices = VEHICLE_TYPES, default = 'Economy')
    special_request = models.CharField(max_length = 300, blank = True)
    sharable = models.BooleanField()
    num_sharer = models.PositiveSmallIntegerField(default = 0, blank = True)
    status = models.CharField(max_length = 15, default = 'open')
    driver_name = models.CharField(max_length = 100, default = '')
    plate_num = models.CharField(max_length = 10, default = '')

    def __str__(self):
        return str(self.username) + ': ' + self.dest_addr + ', ' + self.vehicle_type + ', ' + self.status + ', ' + self.special_request

    
class RideDriver(models.Model):
    username = models.OneToOneField(User, primary_key = True, on_delete = models.CASCADE)
    vehicle_type = models.CharField(max_length = 15, choices = VEHICLE_TYPES)
    plate_num = models.CharField(max_length = 10)
    max_passengers = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    special_request = models.CharField(max_length = 300, blank = True)

    def __str__(self):
        return str(self.username) + ': ' + self.vehicle_type + ', ' + self.plate_num + ', ' + self.special_request
    

class RideSharer(models.Model):
    username = models.ForeignKey(User, on_delete = models.CASCADE)
    owner_id = models.BigIntegerField(default = -1, blank = True)
    dest_addr = models.CharField(max_length = 150)
    arrival_start = models.DateTimeField(default = datetime.now)
    arrival_end = models.DateTimeField(default = datetime.now() + timedelta(hours = 2))
    num_passengers = models.PositiveSmallIntegerField(default = 1, validators=[MinValueValidator(1)])
        
    def __str__(self):
        return str(self.username) + ': ' + self.dest_addr + ', ' + self.num_passengers

    
