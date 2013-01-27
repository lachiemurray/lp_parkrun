from django.core.management.base import BaseCommand 
from lp_parkrun.models import User, Event
from lp_parkrun.scraper import Scraper
from django.conf import settings  
import json

class Command(BaseCommand): 
    
    help = 'Update local parkrun database'

    def handle(self, *args, **options): 

        self.s = Scraper()

        # Scrape for new parkruns 
        events = self.s.scrape_event_ids()

        for e in events:
            if not Event.objects.filter(identifier=e).exists():
                self.add_event(self.s,e)
                
        # Update events
        self.stdout.write('Updating parkruns...\n')
        for event in Event.objects.all():
            self.update_event(event)
            
        # Update users
        self.stdout.write('Updating users...\n')
        for u in User.objects.all():
            self.update_user(u)
        
        self.stdout.write('Done.\n')
        
        
    # Add a new parkrun
    def add_event(self,s,e):    
        
        # Add new event                    
        event = Event(identifier=e)
        
        data = s.scrape_event_data(e)
        
        if data.has_key('name'):
            event.name = data['name']
        else:
            print "Name of event '%s' could not be determined" % e
            return
            
        if data.has_key('number'):
            event.number = data['number']
        else:
            print "Number of runs at '%s' could not be determined" % e
            return
        
        event.save()
        
        print "New event '%s' added!" % event.name
        
        # Add event to meta.json
        f = open(settings.STATIC_ROOT+'meta.json','r')
        meta_data = json.load(f)
        f.close()
        
        options = meta_data['config']['fields'][1]['options']
        
        item = [event.name,event.identifier]
    
        # If an item with this identifier is already in the list, overwrite it
        if e in [x[1] for x in options]:
            options = [item if x[1] == e else x for x in options]
        
        # Otherwise append a new item to the end of the list
        else:
            options.append(item)
        
        # Sort alphabetical
        options.sort()
        
        f = open(settings.STATIC_ROOT+'meta.json','w')
        json.dump(meta_data,f,indent=4)
        f.close()
        
    
    # Update the data of an existing parkrun
    def update_event(self,event):
        
        data = self.s.scrape_event_data(event.identifier)
        
        if data.has_key('number'):
            event.number = data['number']
        else:
            print "Number of runs at '%s' could not be determined" % event.identifier
            return
            
        if not event.postcode:
            event.postcode = self.s.get_event_postcode(event.identifier) or ''
        
        if not event.twitter:
            event.twitter = self.s.get_twitter_id(event.identifier) or ''
        
        event.save()
        
        
    # Update the data of an existing user
    def update_user(self,user):
        
        data = self.s.scrape_user_data(user.athlete_id,user.event_id)
        
        user.total_runs = data.get('total_runs',user.total_runs)
        user.event_runs = data.get('total_runs',user.event_runs)
        user.pb = data.get('pb',user.pb)
        
        user.save()

        
    
