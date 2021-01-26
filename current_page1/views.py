from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import requests
import time

# from .models import city_form

# Create your views here.

data_all = {}
clothing_choice = ""
wearables_choice = ""
sunscreen_choice = ""
colour_code1 = ""
context = {}
all_data = []


# Function for recalculating the wind direction
def wind_direction(winddegree):
    # Replacing winddegree (number) to actual direction
    if 340 < winddegree < 361 or 0 <= winddegree < 20:
        winddirection = "N"
    elif 20 <= winddegree < 70:
        winddirection = "NO"
    elif 70 <= winddegree < 110:
        winddirection = "O"
    elif 110 <= winddegree < 160:
        winddirection = "ZO"
    elif 160 <= winddegree < 200:
        winddirection = "Z"
    elif 200 <= winddegree < 250:
        winddirection = "ZW"
    elif 250 <= winddegree < 291:
        winddirection = "W"
    else:
        winddirection = "NW"
    return winddirection

# Functions for the various weather advices
def clothing_advice():
    current_temperature1 = current_temperature

    if current_temperature1 >= 25:
        clothing_choice = "Het is mooi weer, trek lichte kleding aan"
    elif 20 < current_temperature1 < 25:
        clothing_choice = "Het is lekker weer vandaag, trek iets korts aan"
    elif 18 < current_temperature1 <= 20:
        clothing_choice = "Het is wat kouder weer, trek een lange broek met korte mouwen aan."
    elif 15 < current_temperature1 <= 18:
        clothing_choice = "Het is een middelmatige temperatuur, trek wat dikkere kleding aan."
    elif 5 < current_temperature1 <= 15:
        clothing_choice = "Het is koud, trek warmere kleding aan."
    elif 0 < current_temperature1 <= 5:
        clothing_choice = "Het vriest bijna, trek warme kleding aan en doe misschien handschoenen aan."
    elif -10 < current_temperature1 < 0:
        clothing_choice = "Het vriest, trek dikke kleding aan en doe een muts op als je naar buiten gaat."
    return clothing_choice


def wearables_advice():
    circumstance = current_circumstance
    if circumstance == "sneeuw":
        wearables_choice = "Het sneeuwt, trek sneeuwschoenen aan."
    elif circumstance == "regen en sneeuw":
        wearables_choice = "Het kan gaan regen of sneeuwen, neem een paraplu mee."
    elif circumstance == "regen":
        wearables_choice = "Het gaat regenen, neem een paraplu mee om droog te blijven."
    elif circumstance == "matige regen" or "lichte regen":
        wearables_choice = "Het kan mogelijk een beetje gaan regenen, neem een paraplu mee."
    else:
        wearables_choice = "Het is mooi weer er is geen reden om een accessoire mee te nemen."
    return wearables_choice


def sunscreen_advice():
    uvi = current_uvi
    if 0 <= uvi <= 2:
        sunscreen_choice = "Er is vrijwel geen zon, je hoeft je niet in te smeren."
    elif 2 < uvi <= 4:
        sunscreen_choice = "De zonsterkte is zwak, als je lang buiten bent kan je jezelf met een lichte factor insmeren."
    elif 4 < uvi <= 6:
        sunscreen_choice = "De zon is van matige sterkte. Je huid verbrandt gemakkelijk, dus smeer je in."
    elif 6 < uvi <= 8:
        sunscreen_choice = "De zon is sterk deze dag. Je huid verbrandt makkelijk, dus smeer je goed in."
    elif uvi > 8:
        sunscreen_choice = "De zonsterkte is zeer hoog, smeer je met een goede zonnebrandsfactor in."
    return sunscreen_choice


# Function for the decleration of the colour code of the location
def colour_code():
    # Ask data again
    global colour_code1
    res = requests.get(url2)
    data = res.json()

    # Paramaters for colour code declaration
    daily_maximum_temperature = data["daily"][0]["temp"]["max"]
    hourly_feels_like = data["hourly"][0]["feels_like"]
    visibility = data["hourly"][0]["visibility"]

    try:
        windspeed = current_windspeed
    except NameError:
        windspeed = forecast_windspeed

    # Requirements for the different colour codes
    if windspeed < 75 or daily_maximum_temperature < 35 or hourly_feels_like > -15 or visibility > 200:
        colour_code1 = "Groen"
    elif 75 <= windspeed <= 100 or daily_maximum_temperature > 35 or hourly_feels_like < -15 or visibility < 200:
        colour_code1 = "Geel"
    elif hourly_feels_like < -20 or visibility < 10:
        colour_code1 = "Oranje"
    return colour_code1


# Function for the page not found route
def page_not_found(request):
    # Returning the render of the right html file.
    return render(request, 'current_page1/Place_not_found.html')


# Function for the home page
def pag1(request):
    # Returning the render of the right html file.
    return render(request, 'current_page1/Index.html')


# Function for the current_weather page
def get_current_weather(request):
    global data_all
    # If a place is given inside the html form
    if request.method == 'POST':
        city_name = request.POST["city_name"]
        # city_name = city_form(request.POST)

        # Making sure the program doesn't crash when an invalid place name is given
        try:
            # API key, between the {} in the url will come the city name with the format function
            url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'
            # url1 = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(city_name)

            # Check whether the request got through
            # Ask the data from the Openweathermap website (is in an Json file)
            res = requests.get(url1)
            data1 = res.json()

            # Ask coordinates
            global latitude
            latitude = data1["coord"]["lat"]
            global longitude
            longitude = data1["coord"]["lon"]

            global url2
            url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(
                latitude, longitude)

            # Ask whether the request got trough.
            res = requests.get(url2)
            data2 = res.json()

            # Display the relevant information
            global current_temperature
            current_temperature = data2["current"]["temp"]
            current_humidity = data2["current"]["humidity"]
            global current_circumstance
            current_circumstance = data2["current"]["weather"][0]["description"]
            global current_uvi
            current_uvi = data2["current"]["uvi"]
            current_winddegree = data2["current"]["wind_deg"]
            global current_windspeed
            current_windspeed = data2["current"]["wind_speed"]


            code = colour_code()

            # Clothing advice for the user for this day
            global clothing
            clothing = clothing_advice()

            # Advice for which wearables you should take with you if you go outside
            wearables = wearables_advice()

            # Advice for sunscreen usage based on the uv-index

            sunscreen = sunscreen_advice()

            # Replacing windspeed from m/s to km/u
            current_windspeed = round(current_windspeed * 3.6, 2)

            # Call the function to get a generalised winddirection

            current_winddirection = wind_direction(current_winddegree)

            # Dictionary for all the data
            data_all = {
                'current_temperature': current_temperature,
                'current_humidity': current_humidity,
                'current_circumstance': current_circumstance,
                'current_uvi': current_uvi,
                'current_winddirection': current_winddirection,
                'current_windspeed': current_windspeed,
                'current_clothing_advice': clothing,
                'current_wearables_advice': wearables,
                'current_sunscreen_advice': sunscreen,
                'current_colour_code': code,
            }

        # Other part of the error prevention
        except KeyError:
            data_all = {}


# Function for the filled in city current weather path
def filled_in_current_weather(request):
    get_current_weather(request)
    #return HttpResponse(current_winddirection)
    # Leading the user to a page not found page when an invalid place name is given
    if data_all:
        return render(request, 'current_page1/Current_weather_city.html', data_all)
    else:
        return HttpResponseRedirect('not_found/')


# Function for the weather forecast path
def forecast(request):
    # Returning the render of the right html file
    return render(request, 'current_page1/forecast.html')


# Function for the weather forcast path with city name
def get_weather_forecast(request):
    global all_data
    global context

    # If a place is given inside the html form
    if request.method == 'POST':
        city_name = request.POST["city_name"]
        # city_name = city_form(request.POST)

        # Making sure the program doesn't crash when an invalid place name is given
        try:
            # API key, between the {} in the url will come the city name with the format function
            url1 = 'https://api.openweathermap.org/data/2.5/weather?q=' + city_name + '&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'
            # url1 = 'https://api.openweathermap.org/data/2.5/weather?q={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(city_name)

            # Check whether the request got through
            # Ask the data from the Openweathermap website (is in an Json file)
            res = requests.get(url1)
            data1 = res.json()

            # Ask coordinates
            latitude = data1["coord"]["lat"]
            longitude = data1["coord"]["lon"]


            url2 = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&lang=nl&units=metric&appid=2253466108d70704667b91ffe52d6b16&'.format(
                latitude, longitude)

            # Ask whether the request got trough.
            res = requests.get(url2)
            data = res.json()

            # For the 8 days of weatherforecast
            """for j in range(0, 8):
                # Display the day of the week

                # Display the relevant information
                forecast_temperature = round((data["daily"][j]["temp"]["min"] + data["daily"][j]["temp"]["max"]) / 2, 2)
                forecast_humidity = data["daily"][j]["humidity"]
                forecast_circumstance = data["daily"][j]["weather"][0]["description"]
                forecast_uvi = data["daily"][j]["uvi"]
                forecast_winddegree = data["daily"][j]["wind_deg"]

                # Call the function to get a generalised winddirection
                forecast_winddirection = wind_direction(forecast_winddegree)

                global forecast_windspeed
                forecast_windspeed = data["daily"][j]["wind_speed"]

                # Clothing advice for the user for this day
                #clothing_advice(forecast_temperature)
                # Advice for which wearables you should take with you if you go outside
                #wearables_advice(forecast_circumstance)
                # Advice for sunscreen usage based on the uv-index
                #sunscreen_advice(forecast_uvi)"""

            time_offset = data["timezone_offset"]

            # Dictionary for the data for all the days
            all_data = [
                {
                    'day': time.ctime(data["daily"][0]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][0]["temp"]["min"] + data["daily"][0]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][0]["humidity"],
                    'forecast_circumstance':  data["daily"][0]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][0]["uvi"],
                    'forecast_winddegree': data["daily"][0]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][0]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][1]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][1]["temp"]["min"] + data["daily"][1]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][1]["humidity"],
                    'forecast_circumstance': data["daily"][1]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][1]["uvi"],
                    'forecast_winddegree': data["daily"][1]["wind_deg"],
                    'forecast_windspeed': round(data["daily"][1]["wind_speed"] * 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][2]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][2]["temp"]["min"] + data["daily"][2]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][2]["humidity"],
                    'forecast_circumstance':  data["daily"][2]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][2]["uvi"],
                    'forecast_winddegree': data["daily"][2]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][2]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][3]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][3]["temp"]["min"] + data["daily"][3]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][3]["humidity"],
                    'forecast_circumstance':  data["daily"][3]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][3]["uvi"],
                    'forecast_winddegree': data["daily"][3]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][3]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][4]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][4]["temp"]["min"] + data["daily"][4]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][4]["humidity"],
                    'forecast_circumstance':  data["daily"][4]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][4]["uvi"],
                    'forecast_winddegree': data["daily"][4]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][4]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][5]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][5]["temp"]["min"] + data["daily"][5]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][5]["humidity"],
                    'forecast_circumstance':  data["daily"][5]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][5]["uvi"],
                    'forecast_winddegree': data["daily"][5]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][5]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][6]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][6]["temp"]["min"] + data["daily"][6]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][6]["humidity"],
                    'forecast_circumstance':  data["daily"][6]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][6]["uvi"],
                    'forecast_winddegree': data["daily"][6]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][6]["wind_speed"]* 3.6, 2),
                },
                {
                    'day': time.ctime(data["daily"][7]["dt"] + time_offset),
                    'forecast_temperature': round((data["daily"][7]["temp"]["min"] + data["daily"][7]["temp"]["max"]) / 2, 2),
                    'forecast_humidity': data["daily"][7]["humidity"],
                    'forecast_circumstance':  data["daily"][7]["weather"][0]["description"],
                    'forecast_uvi': data["daily"][7]["uvi"],
                    'forecast_winddegree': data["daily"][7]["wind_deg"],
                    'forecast_windspeed':round(data["daily"][7]["wind_speed"]* 3.6, 2),
                }
            ]

        # Other part of the error prevention
        except IndentationError:
            all_data = []

    context = {'all_data': all_data}
    return context

# Function for the data from the weather forecast for the city.
# This doesn't work quite yet, but we'll finish it in sprint 3.
def filled_in_weather_forecast(request):
    get_weather_forecast(request)
    #return HttpResponse(context)

    return render(request, 'current_page1/forecast_weather_city.html', context)

    """if context:
        return render(request, 'current_page1/forecast_weather_city.html', context)
    else:
        return HttpResponseRedirect('not_found/')"""


# Function for the data from the radar path
def radar(request):
    return render(request, 'current_page1/radar.html')
