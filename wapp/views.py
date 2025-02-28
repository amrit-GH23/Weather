from django.shortcuts import render
import json
import urllib.request
import os
from dotenv import load_dotenv

load_dotenv() 

def index(request):
    if request.method == 'POST':
        api_key = os.getenv("API_KEY")  
        city = request.POST['city']
        
        if api_key:
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
                res = urllib.request.urlopen(url).read()
                json_data = json.loads(res)

                data = {
                    "country_code": str(json_data['sys']['country']),
                    "coordinate": f"{json_data['coord']['lon']} {json_data['coord']['lat']}",
                    "temp": f"{round(json_data['main']['temp'] - 273.15, 2)}°C",
                    "pressure": str(json_data['main']['pressure']),
                    "humidity": str(json_data['main']['humidity']),
                }
            except Exception as e:
                data = {"error": "Invalid city name or API request failed"}
        else:
            data = {"error": "API key is missing"}
    else:
        city = ''
        data = {}

    return render(request, 'index.html', {'city': city, 'data': data})
