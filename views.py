from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import datetime
import hashlib
import json

def create_pub( request, name, barcode, parkrun, date ):
    
    context = { "name" : name, "barcode" : barcode, "parkrun" : parkrun, "date" : date }
        
    response = render(request, 'lp_parkrun/edition.html', context)
    response['ETag'] = hashlib.sha224(name+date).hexdigest()
    
    return response


def edition(request):

    name = "An EXAMPLE"
    barcode = "A12345"
    parkrun = "Bushy Park"
    date = datetime.datetime.now().strftime("%d/%m/%Y")

    return create_pub( request, name, barcode, parkrun, date )


def sample(request):

    name = "An EXAMPLE"
    barcode = "A12345"
    parkrun = "Bushy Park"
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    
    return create_pub( request, name, barcode, parkrun, date )

@csrf_exempt
def validate_config(request):
    
    json_response = {'errors': [], 'valid': True}
    
    response = HttpResponse(json.dumps(json_response), mimetype='application/json')

    return response


# Alternatively, configure webserver to serve this content
def meta_json(request):
    
    return HttpResponseRedirect('/static/meta.json')

# Alternatively, configure webserver to serve this content
def icon(request):
    
    return HttpResponseRedirect('/static/icon.png')
    
    
    
    
    
    
    
    
