import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
# Replace with your OpenWeatherMap API key
API_KEY = '7856dad5b4a3f5e8704bba8ee5ee033f'

def weather_home(request):
    return render(request, 'weather/weather.html')

@require_http_methods(["GET"])
def get_weather(request):
    city = request.GET.get('city', 'London')  # Default to London if no city is provided
    if not city:
        return JsonResponse({'error': 'City not provided'}, status=400)

    # OpenWeatherMap API URL
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if the response contains weather data
        if response.status_code == 200:
            weather_data = {
                'city': data['name'],
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed']
            }
            return JsonResponse(weather_data)
        else:
            return JsonResponse({'error': data.get('message', 'Failed to fetch weather data')}, status=response.status_code)
    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)
