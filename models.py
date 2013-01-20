from django.db import models

class User(models.Model):

    # Global user details
    first_names = models.CharField(max_length=100)
    last_names = models.CharField(max_length=100)
    barcode = models.IntegerField()
    total_runs = models.IntegerField()
    
    # Event specific details
    event_id = models.CharField(max_length=100)
    event_runs = models.IntegerField()
    
    
class Event(models.Model):

    identifier = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    number = models.IntegerField()
    
    twitter = models.CharField(max_length=100,blank=True)
    postcode = models.CharField(max_length=10,blank=True)
    