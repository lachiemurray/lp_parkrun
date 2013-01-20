import json
import urllib2
from django.conf import settings
class Weather:
  content_url="http://free.worldweatheronline.com/feed/weather.ashx?format=json&num_of_days=2"
  
  icon=''
  forecast=''
  temperature=''
  
  def __init__(self, location):
    self.location = location
  
  
  def get_weather(self):
    url = self.content_url+"&q="+self.location+"&key="+settings.WEATHER_KEY
    print url
    doc=urllib2.urlopen(url)
    weather=json.loads(doc.read())
    
    self.icon=self.get_icon_for_key(weather["data"]["current_condition"][0]['weatherCode'])
    self.forecast_string=weather["data"]["current_condition"][0]['weatherDesc'][0]['value']
    self.temperature=weather["data"]["current_condition"][0]['temp_C']

  def get_icon_for_key(self, key):
    weather_types_mapping = {
      "248":"fog",
      "260" : "fog",

      # Heavy cloud
      "122" : "heavy_cloud",

      # Heavy rain
      "302" : "heavy_rain",
      "308" : "heavy_rain",
      "359" : "heavy_rain",

      # Heavy showers
      "299" : "heavy_showers",
      "305" : "heavy_showers",
      "356" : "heavy_showers",

        # Heavy snow showers
      "335" : "heavy_snow_showers",
      "371" : "heavy_snow_showers",
      "395" : "heavy_snow_showers",

        # Heavy snow
      "230" : "heavy_snow",
      "329" : "heavy_snow",
      "332" : "heavy_snow",
      "338" : "heavy_snow",

        # Light cloud
      "119" : "light_cloud",

        # Light rain
      "266" : "light_rain",
      "293" : "light_rain",
      "296" : "light_rain",


        # Light showers
      "176" : "light_showers",
      "263" : "light_showers",
      "353" : "light_showers",

        # Light snow showers
      "323" : "light_snow_showers",
      "326" : "light_snow_showers",
      "368" : "light_snow_showers",

        # Light snow
      "227" : "light_snow",
      "320" : "light_snow",

        # Mist
      "143" : "mist",

        # Sleet showers
      "179" : "sleet_showers",
      "362" : "sleet_showers",
      "365" : "sleet_showers",
      "374" : "sleet_showers",

        # Sleet
      "182" : "sleet",
      "185" : "sleet",
      "281" : "sleet",
      "284" : "sleet",
      "311" : "sleet",
      "314" : "sleet",
      "317" : "sleet",
      "350" : "sleet",
      "377" : "sleet",

      "116" : "sunny_intervals",
      "113" : "sunny",

        #Thunder shower
      "200" : "thundery_showers",
      "386" : "thundery_showers",
      "392" : "thundery_showers",

        #Thunder
      "389" : "thunder"
    }
    return weather_types_mapping[key]