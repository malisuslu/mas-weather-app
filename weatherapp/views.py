from django.shortcuts import render
import requests
from decouple import config
from pprint import pprint
from datetime import datetime

# Create your views here.
def index(request):

    API_KEY = config('API_KEY')
    GOOGLE_API_KEY = config('GOOGLE_API_KEY')
    city = request.POST.get('city') or 'Ankara'

    url_week = 'https://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric'.format(city, API_KEY)

    r_week = requests.get(url_week).json()

    url_today = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric'.format(city, API_KEY)

    r_today = requests.get(url_today).json()


    if r_today['cod'] == 200 and r_week:

        week_days = []
        icons = []
        temps = []
        for i in range(0, 40, 8):
            week_days.append(datetime.fromtimestamp(r_week['list'][i]['dt']).strftime('%a'))
            icons.append(r_week['list'][i]['weather'][0]['icon'])
            temps.append(r_week['list'][i]['main']['temp'])

        context = {
            'city': r_today['name'].title() + ', ' + r_today['sys']['country'],
            'date': datetime.fromtimestamp(r_today['dt']).strftime('%d %b %y %a'),
            'desc': r_today['weather'][0]['description'].title(),
            'temp': r_today['main']['temp'],
            'feel': r_today['main']['feels_like'],
            'min': r_today['main']['temp_min'],
            'max': r_today['main']['temp_max'],
            'rain': r_today['rain']['1h'] if 'rain' in r_today else 0,
            'pressure': r_today['main']['pressure'],
            'humidity': r_today['main']['humidity'],
            'wind': r_today['wind']['speed'],
            'icon': r_today['weather'][0]['icon'],
            'week_days': week_days,
            'icons': icons,
            'temps': temps,
            'lat': r_today['coord']['lat'],
            'lon': r_today['coord']['lon'],
            'google_api_key': GOOGLE_API_KEY,
        }
    else:
        context = {
            'city': 'Region not found',
            'date':  datetime.now().strftime('%d %b %y %a'),
            'desc': '',
            'temp': '',
            'feel': '',
            'min': '',
            'max': '',
            'pressure': '',
            'humidity': '',
            'wind': '',
            'icon': '',
            'country': '',
            'sunrise': '',
            'sunset': '',
            'week_days': '',
            'icons': [ 'No-img' for i in range(5)],
            'temps': '',
            'lat': '',
            'lon': '',
            'google_api_key': GOOGLE_API_KEY,
        }

    return render(request, 'weatherapp/index.html', context)