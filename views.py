from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from lp_parkrun.scraper import Scraper
from models import User, Event
from weather import Weather
import datetime
import hashlib
import json

def edition(request):

    if not request.GET.get('barcode', False):
        return HttpResponse("No barcode was provided", status=400)
    
    # Get user and event
    code = request.GET['barcode']
    user = get_object_or_404(User, barcode=code)
    event = get_object_or_404(Event, identifier=user.event_id)
    
    # Get barcode url    
    barcode_url = "https://service.parkrun.org.uk/runnerSupport/BarcodeImagery/image.php?code=A"+code

    ### User data ###
    user_data = { 'first_name'  : user.first_names.split()[0], 
                  'full_name'   : user.first_names+user.last_names.upper(), 
                  'event_runs'  : user.event_runs+1, 
                  'total_runs'  : user.total_runs+1, 
                  'barcode_url' : barcode_url }

    ### Event data ###
    
    # If event name to long - create a shorter version
    short_name = event.name
    if len(event.name) > 15:
        short_name = event.name.split()[0]
        
    date = datetime.datetime.now().strftime("%d/%m/%Y")

    event_data = { 'short_name' : short_name, 
                   'long_name'  : event.name,
                   'date'       : date, 
                   'number'     : event.number+1 }

    # Create minimal context
    context = { 'user'    : user_data,
                'event'   : event_data }

    ### Weather data ###
    if event.postcode:
        
        # Find weather based upon first part of postcode
        weather = Weather(event.postcode.split()[0])
        weather.get_weather()
        
        weather_data = { 'icon'     : weather.icon,
         	                'postcode' : event.postcode,
                         'text'     : weather.forecast_string, 
                         'temp'     : weather.temperature }
        
        context['weather'] = weather_data

    ### Twitter data ###
    if event.twitter:
        pass

    # Create response
    response = render(request, 'lp_parkrun/edition.html', context)

    # Create ETag
    response['ETag'] = hashlib.sha224(str(user.barcode)+date).hexdigest()
    
    return response


def sample(request):
    
    # Sample data
    user_data = { 'first_name'  : 'Paul', 
                  'full_name'   : 'Paul SINTON-HEWITT', 
                  'event_runs'  : 29, 
                  'total_runs'  : 65, 
                  'barcode_url' : '/static/barcode_images/sample.gif' }
    
    event_data = { 'short_name' : 'Bushy Park', 
                   'long_name'  : 'Bushy Park',
                   'date'       : '28/07/2012', 
                   'number'     : 421 }
    
    weather_data = { 'icon'     : 'sunny', 
                     'postcode' : 'TW11 0EQ', 
                     'text'     : 'clear blue skies', 
                     'temp'     : 18 }
    
    twitter_data = { 'id'   : 'bushyparkrun', 
                     'text' : '''Don't forget that we're not running today. Why 
                              not try another parkrun instead or come along to 
                              Bushy to cheer on the cyclists. #london2012''' }

    context = { 'user'    : user_data,
                'event'   : event_data,
                'weather' : weather_data,
                'twitter' : twitter_data }
        
    # Create response
    response = render(request, 'lp_parkrun/edition.html', context)
    
    return response

@csrf_exempt
def validate_config(request):
    
    json_response = { 'errors': [], 'valid': True }
    scraper = Scraper()

    # Extract config from POST
    user_settings = json.loads(request.raw_post_data)['config']
    barcode = user_settings.get('barcode', None)
    event = user_settings.get('event', None)
    
    # Check that the user entered a barcode
    if barcode:
        
        # Check that the barcode represents an integer
        try:
            # If necessary, remove leading 'A'
            barcode = int(barcode.strip('A'))       
        except:
            json_response['valid'] = False
            json_response['errors'].append('Your barcode should only contain numbers')
        
        if type(barcode) is int:
            
            # Check that the barcode is recognised
            if not Scraper.is_barcode_valid(barcode):
                json_response['valid'] = False        
                json_response['errors'].append('The barcode you entered was not recognised')
    
    else:
        json_response['valid'] = False
        json_response['errors'].append('Please enter a barcode.')
    
    # Check that the user selected an event
    if event:
#       # Check that the event is valid - should only fail here if the parkrun 
        # website is down, or the event names in meta.json are out of date
        if not Scraper.is_event_valid(event):
            json_response['valid'] = False
            json_response['errors'].append('The event you selected was not recognised, please select another event or try again later')
                
    else:
        json_response['valid'] = False
        json_response['errors'].append('Please select an event from the select box')
        
    # Add/update user in database
    if json_response['valid']:
        
        # Update an existing user or create a new one
        user = User.objects.get_or_create(barcode=barcode)
        user.event_id = event
        
        # Get user data
        data = scraper.scrape_user_data(barcode, event)
        
        user.first_names = data.get('first_names','')
        user.last_names = data.get('last_names','')
        user.event_runs = data.get('event_runs',0)
        user.total_runs = data.get('total_runs',0)
        user.pb = data.get('pb',0)

        if len(user.first_names) and len(user.last_names):
            user.save()
        else:
            json_response['valid'] = False
            json_response['errors'].append('There was a problem retrieving your information. Please try again later')      
    
    response = HttpResponse(json.dumps(json_response), mimetype='application/json')

    return response


# Alternatively, configure webserver to serve this content
def meta_json(request):
    
    return HttpResponseRedirect('/static/meta.json')

# Alternatively, configure webserver to serve this content
def icon(request):
    
    return HttpResponseRedirect('/static/icon.png')
    
