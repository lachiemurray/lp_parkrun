from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from Models import User, Event

import datetime
import hashlib
import json


def create_pub( request, code ):
    
    
    # Get user
    user = get_object_or_404(User, barcode=code)
    
    # Get event
    event = get_object_or_404(Event, identifier=user.event_id)
    
    # Generate weather
    weather = render_to_string("lp_parkrun/weather.html", { "icon":"icon.png" } )
    
    context = { "user" : user, "event" : event, "weather": weather }
    
    response = render(request, 'lp_parkrun/edition.html', context)
    
    # Create ETag
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    response['ETag'] = hashlib.sha224(str(user.barcode)+date).hexdigest()
    
    return response


def edition(request):

    barcode = 12345
    return create_pub( request, barcode )


def sample(request):

    barcode = 12345
    return create_pub( request, barcode )

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
    
    
    
    
    
    
    
    
