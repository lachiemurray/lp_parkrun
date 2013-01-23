from datetime import datetime
import urllib2
import re

class Scraper():
    
    def __init__(self):
        
        self.user_agent = "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"
        
        # Compile regexs
        self.event_re = re.compile("<h2>([a-zA-Z\s\.\-&;']*)parkrun.*#\s*([0-9]+)")
        self.postcode_re = re.compile('([A-PR-UWYZ0-9][A-HK-Y0-9][AEHMNPRTVXY0-9]?[ABEHMNPRVWXY0-9]? {1,2}[0-9][ABD-HJLN-UW-Z]{2}|GIR 0AA)')
        self.event_id_re = re.compile('<a href="http:\/\/www.parkrun.org.uk\/([a-zA-Z\-]*)\/results">')
        
        self.user_pb = re.compile('<td>Time</td><td>([0-9]+:[0-9]+)<\/td>')
        self.user_re = re.compile('<h2>(.*)</h2>',flags=re.DOTALL)
        self.user_name_re = re.compile('(?=.*-)([A-Z]{1}[a-zA-Z\-]+)\s')
        self.user_runs = re.compile('(?P<event_runs>[0-9]+).*at\s(?P<event>.*)<br\/>(?P<total_runs>[0-9]+)')

    # Scrape parkrun website and return a list of all parkrun events
    def scrape_event_ids(self):
        print 'Looking for new parkruns...'  
    
        request = urllib2.Request("http://www.parkrun.org.uk/results/attendancerecords/")
        request.add_header("User-Agent", self.user_agent)
    
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError as detail:
            print "Error opening URL %s: %s" % (request.get_full_url(), detail)
            return []
        
        events_page = f.read()
        
        event_ids = self.event_id_re.findall(events_page)
      
        return event_ids
            
    # Scrape basic user data
    def scrape_user_data(self, barcode, event):
        print "Scraping user '%s'" % barcode
        
        # Dictionary for storing data
        user_data = dict()
        
        request = urllib2.Request("http://www.parkrun.org.uk/"+event+"/results/athletehistory/?athleteNumber="+str(barcode))
        request.add_header("User-Agent",self.user_agent)
        
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError as detail:
            print "Error opening URL %s: %s" % (request.get_full_url(), detail)
            return user_data
        
        page = f.read()
    
        # Isolate the most important section of the page       
        result = self.user_re.search(page)
        
        if result:
            if result.group(1):
                user = result.group(1)               
        
        
        ### Scrape names ###
        
        result = self.user_name_re.findall(user)
        
        first_names = ''
        last_names = ''
        
        for r in result:
            
            # Last names are provided in upper case
            if r.isupper():
                last_names=last_names+r+' '
            else:
                first_names=first_names+r+' '
                
        user_data['first_names'] = first_names.strip()
        user_data['last_names'] = last_names.title()
        
        
        ### Scrape runs ###
        
        result = self.user_runs.search(user)
                         
        if result:
            
            # Set to zero by default
            user_data['event_runs']=0
                
            # Check if user has run at this event before
            if result.group('event').strip() != "All Events":
                if result.group('event_runs'):
                    user_data['event_runs']=int(result.group('event_runs'))
                        
            if result.group('total_runs'):
                user_data['total_runs']=int(result.group('total_runs'))   
        
        
        ### Scrape PB ###
        result = self.user_pb.search(page)
                
        if result:
            
            # Set to zero by default
            user_data['pb']=0
            
            if result.group(1):
                pb = datetime.strptime(result.group(1),"%M:%S")
                user_data['pb'] = pb.second + 60 * pb.minute
        
        return user_data
        
        
                
    # Scrape basic event data
    def scrape_event_data(self, identifier):
        print "Scraping event '%s'" % identifier
        
        # Create dictionary for storing data
        event_data = dict()
        
        request = urllib2.Request("http://www.parkrun.org.uk/"+identifier+"/results/latestresults")
        request.add_header("User-Agent",self.user_agent)
        
        try:
            f = urllib2.urlopen(request)
        except urllib2.HTTPError as detail:
            print "Error opening URL %s: %s" % (request.get_full_url(), detail)
            return event_data
        
        ### Scrape name and number ###
        
        result = self.event_re.search(f.read())
      
        if result:
            if result.group(1):
                event_data['name'] = result.group(1).strip()
            
            if result.group(2):
                event_data['number'] = int(result.group(2))
        
        return event_data
    
    # Try to find an event's postcode   
    def get_event_postcode(self,identifier):
        print "Getting postcode '%s'" % identifier

        request = urllib2.Request("http://www.parkrun.org.uk/"+identifier+"/course/")
        request.add_header("User-Agent",self.user_agent)
        
        try:   
            f = urllib2.urlopen(request)
        except urllib2.HTTPError as detail:
            print "Error opening URL %s: %s" % (request.get_full_url(), detail)
            return None
          
        postcode = self.postcode_re.findall(f.read())

        if postcode:
            return postcode[0]
     
    # Try to work out an event's twitter id   
    def get_twitter_id(self,identifier):
        print "Getting twitter id '%s'" % identifier
        
        # TODO: check if suggested id is longer than
        #     15 chars, and if so remove some vowels
        
        usernames = [identifier+'parkrun',identifier+'parkrunUK']

        for u in usernames:
            
            request = urllib2.Request("http://www.twitter.com/"+u)
            request.add_header("User-Agent",self.user_agent)
            
            try:
                result = urllib2.urlopen(request)  
            except urllib2.HTTPError as detail:
                print "Error opening URL %s: %s" % (request.get_full_url(), detail)
                continue
            
            if result.getcode() == 200:
                return u
            