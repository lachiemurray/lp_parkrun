from django.core.management.base import BaseCommand, CommandError 
from lp_parkrun.models import User, Event

class Command(BaseCommand): 
    
    help = 'Update local parkrun database'

    def handle(self, *args, **options): 

        # Scrape for new parkruns 
        events = ScrapeEvents()
        
        for e in events:
    	       if not Event.objects.filter(identifier=e).exists():
                 # Add new event
                 event = Event(identifier=e)
                 event.scrape_event_data()
                 #event.save()
                 
        # Update events
        self.stdout.write('Updating parkruns...\n')
        for e in Event.objects.all():
            e.scrape_event_data()
            #e.save()
    
        # Update users
        self.stdout.write('Updating users...\n')
        for u in User.objects.all():
            u.scrape_user_data()
            #u.save()
        
        self.stdout.write('Done.\n')
        
        
# Scrape parkrun website and return a list of all parkrun events
def ScrapeEvents():

    print 'Looking for new parkruns...'    
    return ['mileend', 'york', 'bushy', 'harrogate']
