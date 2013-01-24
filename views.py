from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
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

    ### User data ###
    user_data = { 'first_name' : user.first_names.split()[0], 
                  'full_name'  : user.first_names+user.last_names.upper(), 
                  'event_runs' : user.event_runs+1, 
                  'total_runs' : user.total_runs+1, 
                  'barcode'    : user.barcode }

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
        
        weather_data = { 'icon' : weather.icon, 
                         'text' : weather.forecast_string, 
                         'temp' : weather.temperature }
        
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
    user_data = { 'first_name' : 'Paul', 
                  'full_name'  : 'Paul SINTON-HEWITT', 
                  'event_runs' : 29, 
                  'total_runs' : 65, 
                  'barcode'    : 'SAMPLE' }
    
    event_data = { 'short_name' : 'Bushy Park', 
                   'long_name'  : 'Bushy Park',
                   'date'       : '28/07/2012', 
                   'number'     : 421 }
    
    weather_data = { 'icon' : 'sunny', 
                     'text' : 'clear blue skies', 
                     'temp' : 18 }
    
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

    # Check that barcode exists
    
    
    # Add/update user in database


    
    response = HttpResponse(json.dumps(json_response), mimetype='application/json')

    return response


# Alternatively, configure webserver to serve this content
def meta_json(request):
    
    return HttpResponseRedirect('/static/meta.json')

# Alternatively, configure webserver to serve this content
def icon(request):
    
    return HttpResponseRedirect('/static/icon.png')
    
