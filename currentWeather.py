try:
    import requests
    import dateutil.parser
except ModuleNotFoundError:
    print("Install all the requirements first!")
    print("See github page for the requirements!")
    exit()

apikey = "GET IT FROM ACCUWEATHER!!!!!!"

"""Ask for a city"""
city = input("Enter the city: ")
"""Search  for the city"""
try:
    cityList = requests.get("http://dataservice.accuweather.com/locations/v1/cities/search?apikey="+apikey+"&q="+city)
except ConnectionError:
    print("Check Your Internet connection")
    exit()
"""Give a list and ask for the correct one(if there is only one response, proceed without confirmation)"""
i = 0
print(cityList.json())
if not cityList.json():
    print("There is no city with name - "+city)
else:
    print("Choose a Place From The following list: ")
    for xcity in cityList.json():
        i+=1
        print(str(i)+".\t"+xcity['Type']+": "+xcity['EnglishName']+"\n\t"+xcity['AdministrativeArea']['EnglishType']+": "+xcity['AdministrativeArea']['EnglishName']+"\n\tCountry: "+xcity['Country']['EnglishName'])
    while(True):
        try:
            choice = int(input("Choice: "))
            choice -=1
            if choice<0:
                raise IndexError
            break
        except IndexError:
            print("Enter a value from the choices")
        except ValueError:
            print("Enter a valid integer")
"""Show the user current temprature, weather text"""
try:
    currentConditions = requests.get("http://dataservice.accuweather.com/currentconditions/v1/"+cityList.json()[choice]['Key']+"?apikey="+apikey+"&details=true")
except ConnectionError:
    print("Check Your Internet connection.")
    exit()
print("\nCurrent Conditions of "+cityList.json()[choice]['EnglishName']+","+cityList.json()[choice]['AdministrativeArea']['EnglishName']+","+cityList.json()[choice]['Country']['EnglishName']+" :")
print("Description: "+currentConditions.json()[0]['WeatherText'])
print("Temperature: "+str(currentConditions.json()[0]['Temperature']['Metric']['Value'])+"°C")
print("Relative Humidity: "+str(currentConditions.json()[0]['RelativeHumidity'])+"%")
print("Wind:\n\tSpeed: "+str(currentConditions.json()[0]['Wind']['Speed']['Metric']['Value'])+"km/h\n\tDirection: "+currentConditions.json()[0]['Wind']['Direction']['English']+"\n\tDegree: "+str(currentConditions.json()[0]['Wind']['Direction']['Degrees']))
#print("For more info: "+currentConditions.json()[0]['Link'])
"""Five days forcast"""
try:
    fiveDay = requests.get("http://dataservice.accuweather.com/forecasts/v1/daily/5day/"+cityList.json()[choice]['Key']+"?apikey="+apikey+"&details=true&metric=true")
except ConnectionError:
    print("Check your internet connection")
    exit()

## I'll provide temperature here
print("\nFive Day forcast:")
print("Headline for 5 days: "+fiveDay.json()['Headline']['Text'])
for dateData in fiveDay.json()['DailyForecasts']:
    dateToday = dateutil.parser.parse(dateData['Date'])
    print("Date: "+dateToday.strftime("%d,%B(%A)"))
