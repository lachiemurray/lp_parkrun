from django.core.management.base import BaseCommand, CommandError 
from lp_parkrun.models import User, Event
import urllib2
import re

class Command(BaseCommand): 
    
    help = 'Update local parkrun database'

    def handle(self, *args, **options): 

        # Scrape for new parkruns 
        events = ScrapeEvents()
            
        for e in events:
            if not Event.objects.filter(identifier=e).exists():
                # Add new event
                try:
                    event = Event(identifier=e)
                    event.scrape_event_data()
                    event.save()
                    
                    # Add to meta.json
                except:
                    print "Problem adding %s to database" % e

        # Update events
        self.stdout.write('Updating parkruns...\n')
        for e in Event.objects.all():
            e.scrape_event_data()
            e.save()
    
        # Update users
        self.stdout.write('Updating users...\n')
        for u in User.objects.all():
            u.scrape_user_data()
            #u.save()
        
        self.stdout.write('Done.\n')
        
        
# Scrape parkrun website and return a list of all parkrun events
def ScrapeEvents():

    user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
    event_pattern = '<a href="http:\/\/www.parkrun.org.uk\/([a-zA-Z\-]*)\/results">'

    print 'Looking for new parkruns...'  
    
    request = urllib2.Request("http://www.parkrun.org.uk/results/attendancerecords/")
    request.add_header("User-Agent", user_agent)
    
    f = urllib2.urlopen(request)
    events_page = f.read()
        
    events = re.findall(event_pattern, events_page)
      
    return events
