from models import User, Event

def ScrapeEvents():

    print 'Looking for new parkruns...'
    
    return ['mileend', 'york', 'bushy', 'harrogate']
    

def AddEvent(event_id):
    
    # Scrape event page

    print 'Adding "%s"' % event_id
    

def UpdateEvent(event):
    print 'Updating %s' % event.full_name
    pass

def AddUser(barcode):
    print 'Adding "%d"' % barcode
    pass
    
    
def UpdateUser(user):
    print 'Updating %s %s' % (user.first_names, user.last_names)
    pass
    