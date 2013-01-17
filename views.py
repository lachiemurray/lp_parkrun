from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import dateutil.parser
import hashlib
import json

greetings = {"english" : ["Good morning", "Hello", "Good evening"], 
    "french" : ["Bonjour", "Bonjour", "Bonsoir"], 
    "german" : ["Guten morgen", "Hallo", "Guten abend"], 
    "spanish" : ["Buenos d&#237;as", "Hola", "Buenas noches"], 
    "portuguese" : ["Bom dia", "Ol&#225;", "Boa noite"], 
    "italian" : ["Buongiorno", "ciao", "Buonasera"], 
    "swedish": ["God morgon", "Hall&#229;", "God kv&#228;ll"]}

def edition(request):

    # Check for required vars
    if not request.GET.get('local_delivery_time',False):
        return HttpResponse("Error: No local_delivery_time was provided", status=400)
        
    if not request.GET.get('lang', False):
        return HttpResponse("Error: No lang was provided", status=400)
        
    if not request.GET.get('name', False):
        return HttpResponse("No name was provided", status=400)

    # Extract configuration provided by user through BERG Cloud. These options are defined by the JSON in meta.json.
    date = dateutil.parser.parse(request.GET['local_delivery_time'])
    if not date.weekday() == 0:
        return HttpResponse("It is not a Monday", status=406)
    
    # Get config
    language = request.GET['lang']
    name = request.GET['name']
    
    # Pick a time of day appropriate greeting
    i = 0
    if date.hour >= 12 and date.hour <=17:
        i = 1
    if (date.hour > 17 and date.hour <=24) or (date.hour >= 0 and date.hour <= 3):
        i = 2

    greeting = "%s, %s" % (greetings[language][i], name)
        
    # Set the etag to be this content. This means the user will not get the same content twice, 
    # but if they reset their subscription (with, say, a different language they will get new content 
    # if they also set their subscription to be in the future)
    context = { 'greeting' : greeting }
    response = render(request, 'lp_hello_django/hello_world.html', context)
    response['ETag'] = hashlib.sha224(language+name+date.strftime('%d%m%Y')).hexdigest()

    return response


def sample(request):

    # Sample data
    language = 'english';
    name = 'Little Printer';
    greeting = "%s, %s" % (greetings[language][0], name)
 
    # Create response
    context = {'greeting' : greeting}
    response = render(request, 'lp_hello_django/hello_world.html', context)
    response['ETag'] = hashlib.sha224(language+name).hexdigest()
    
    return response

@csrf_exempt
def validate_config(request):
    
    json_response = {'errors': [], 'valid': True}

    # Extract config from POST
    user_settings = json.loads(request.raw_post_data)['config']
    
    # If the user did choose a language:
    if not user_settings.get('lang', None):
        json_response['valid'] = False
        json_response['errors'].append('Please select a language from the select box.')

    # If the user did not fill in the name option:
    if not user_settings.get('name', None):
        json_response['valid'] = False
        json_response['errors'].append('Please enter your name into the name box.')

    # Is a valid language set?
    if user_settings.get('language', None) in greetings:
        json_response['valid'] = False
        json_response['errors'].append("We couldn't find the language you selected (%s) Please select another" % user_settings['language'])
    
    # Create response
    response = HttpResponse(json.dumps(json_response), mimetype='application/json')

    return response


# Alternatively, configure webserver to serve this content
def meta_json(request):
    
    return HttpResponseRedirect('/static/meta.json')

# Alternatively, configure webserver to serve this content
def icon(request):
    
    return HttpResponseRedirect('/static/icon.png')
    
    
    
    
    
    
    
    
