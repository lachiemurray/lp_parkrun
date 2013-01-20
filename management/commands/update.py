from django.core.management.base import BaseCommand, CommandError 
from lp_parkrun.models import User, Event

from lp_parkrun.tools import * 

class Command(BaseCommand): 
    
    help = 'Update local parkrun database'

    def handle(self, *args, **options): 

        # Scrape for new parkruns 
        self.stdout.write('Looking for new parkruns...\n')
    
    
    
        events = ['mileend', 'york', 'bushy', 'harrogate']
        for e in events:
    	       if not Event.objects.filter(identifier=e).exists():
                 AddEvent(e)
    
        # Update events
        self.stdout.write('Updating parkruns...\n')
        for e in Event.objects.all():
            UpdateEvent(e)
    
        # Update users
        self.stdout.write('Updating users...\n')
        for u in User.objects.all():
            UpdateUser(u)
        
        self.stdout.write('Done.\n')