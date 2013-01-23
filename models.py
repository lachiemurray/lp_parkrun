from django.db import models

class User(models.Model):

    # Global user details
    first_names = models.CharField(max_length=100)
    last_names = models.CharField(max_length=100)
    barcode = models.IntegerField()
    total_runs = models.IntegerField()
    
    # Event specific details
    pb = models.IntegerField(default=0)
    event_id = models.CharField(max_length=100)
    event_runs = models.IntegerField()
    
    def __unicode__(self):
        return self.first_names+" "+self.last_names
        
    
class Event(models.Model):

    # Event details
    identifier = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    
    # Optional details
    twitter = models.CharField(max_length=100,blank=True)
    postcode = models.CharField(max_length=10,blank=True)
    
    def __unicode__(self):
        return self.name
    
    def has_twitter_id(self):
        return len(self.twitter) > 0
    has_twitter_id.boolean = True
    has_twitter_id.admin_order_field = 'twitter'
    has_twitter_id.short_description = 'Twitter ID defined'
    
    def has_postcode(self):
        return len(self.postcode) > 0
    has_postcode.boolean = True
    has_postcode.admin_order_field = 'postcode'
    has_postcode.short_description = 'Postcode defined'
    

