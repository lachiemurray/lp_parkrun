from django.db import models
import urllib2
import re
from django.template.defaultfilters import default

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
    
    def scrape_event_data(self):

        user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"                
        
        print "Scraping event '%s'" % self.identifier
        
        # Find out how many runs there have been
        run_num_pattern = "<h2>([a-zA-Z\s\.\-&;']*)parkrun.*#\s*([0-9]+)"

        request = urllib2.Request("http://www.parkrun.org.uk/"+self.identifier+"/results/latestresults")
        request.add_header("User-Agent",user_agent)
    
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError as detail:
            print detail
            return
        
        history_page = f.read()
        result = re.search(run_num_pattern, history_page)
               
        if result: 
            if result.group(2):
                self.number = int(result.group(2))
            
            if not self.name and result.group(1):
                self.name = result.group(1).strip()            
        
        if not self.postcode:
             
            # Try to find the event's postcode    
            post_code_pattern = '([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)'        
    
            request = urllib2.Request("http://www.parkrun.org.uk/"+self.identifier+"/course/")
            request.add_header("User-Agent",user_agent)
            
            f = urllib2.urlopen(request)
            course_page = f.read()
            
            postcode = re.findall(post_code_pattern, course_page)
            
            if postcode:
                self.postcode = postcode[0]

        if not self.twitter:
        
            # Try to work out the event's twitter id
            try:
                twitter_add = 'http://www.twitter.com/'+self.identifier+'parkrun'        
                result = urllib2.urlopen(twitter_add)    
    
                if( result.getcode() == 200 ):
                    self.twitter = self.identifier+'parkrun'
            except:
                pass               
            

        
        
        
        

