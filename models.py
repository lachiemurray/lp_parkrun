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
    
    def __unicode__(self):
        return self.first_names+" "+self.last_names
    
    def scrape_user_data(self):
        print "Scraping user '%s'" % self.barcode
        
    
class Event(models.Model):

    # Event details
    identifier = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    number = models.IntegerField()
    
    # Optional details
    twitter = models.CharField(max_length=100,blank=True)
    postcode = models.CharField(max_length=10,blank=True)
    
    def __unicode__(self):
        return self.full_name
    
    def scrape_event_data(self):
        print "Scraping event '%s'" % self.identifier
        
    
    
        
         