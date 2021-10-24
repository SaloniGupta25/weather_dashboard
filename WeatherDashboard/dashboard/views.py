from django.shortcuts import render
from django.http import HttpResponse
from .forms import CityForm

import requests


def home(request):
    form = CityForm()

    if request.method =='POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            city_name=form.cleaned_data.get('city_name')
            url='https://api.openweathermap.org/data/2.5/weather'
            params={
               'q':city_name,
               'appid':'0c42fc380f0096d16f47554c3749554e',
                'units':'metric',
             }
            response=requests.get(url,params=params)
            json_response = response.json()
            weather_data={
                'temp': json_response['main']['temp'],
                'temp_min':json_response['main']['temp_min'],
                'temp_max':json_response['main']['temp_max'],
                'city_name':json_response['name'],
                'country':json_response['sys']['country'],
                'lat':json_response['coord']['lat'],
                'lon':json_response['coord']['lon'],
                'Weather':json_response['weather'][0]['main'],
                'weather_desc':json_response['weather'][0]['description'],
                'pressure':json_response['main']['pressure'],
                'humidity':json_response['main']['humidity'],
                'wind_speed':json_response['wind']['speed'],
            }
    elif request.method=="GET":
        weather_data=None
    template_name='home.html'
    context={'form':form,'weather_data':weather_data}
    return render(request,template_name,context=context)

