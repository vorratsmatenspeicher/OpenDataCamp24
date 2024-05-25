from openmeteopy import OpenMeteo
from openmeteopy.options import DwdOptions
from openmeteopy.hourly import HourlyDwd
import re


def indexesfromregex(dic: list, regex: str) -> list:
    p = re.compile(regex)
    indecies = []
    for i in dic:
        v = str(i)
        if p.match(v):
            indecies.append(dic.index(i));
    return indecies


def getListFromIndex(meteo: dict, valuelist: str, indexlist: list) -> list:
    res = []
    for i in indexlist:
        res.append((meteo["hourly"]["time"][i], meteo["hourly"][valuelist][i]))
    return res


def getHourlyValuesOfDay(meteo: dict, day: str, output: str) -> list:
    return getListFromIndex(meteo, output, indexesfromregex(meteo["hourly"]["time"], day + "T[0-3][0-9]:00")) 


def getWeatherCodeString(code: int) -> str:
    match code: 
        case 0:
            return "Clouds: Clear"
        case 1:
            return "Clouds: Mainly clear"
        case 2: 
            return "Clouds: Partly"
        case 3:
            return "Clouds: Overcast"
        case 45:
            return "Fog: Normal"
        case 48:
            return "Fog: Deposition of frost"
        case 51:
            return "Drizzle: Light intensity"
        case 53:
            return "Drizzle: Moderate intensity"
        case 55:
            return "Drizzle: Dense intensity"
        case 56:
            return "Freezing Drizzle: Light intensity"
        case 57:
            return "Freezing Drizzle: Dense intensity"
        case 61:
            return "Rain: Slight intensity"
        case 63: 
            return "Rain: Moderate intensity"
        case 65:
            return "Rain: Heavy intensity"
        case 66:
            return "Freezing Rain: Light intensity"
        case 67:
            return "Freezing Rain: Heavy intensity"
        case 71:
            return "Snow fall: Slight intensity"
        case 73:
            return "Snow fall: Moderate intensity"
        case 75: 
            return "Snow fall: Heavy intensity"
        case 77:
            return "Snow fall: Snow grains"
        case 80:
            return "Rain showers: Slight"
        case 81:
            return "Rain showers: Moderate"
        case 82:
            return "Rain showers: Violent"
        case 85:
            return "Snow showers: Slight"
        case 86:
            return "Snow showers: Heavy"
        case 95:
            return "Thunderstorm: Slight or moderate"
        case 96:
            return "Thunderstorm: with slight hail"
        case 99:
            return "Thunderstorm: with heavy hail"


def get_weather_forcast(longitude: float, latitude: float, day: str, output: str) -> list:
    hourly = HourlyDwd()
    options = DwdOptions(latitude, longitude)

    mgr = OpenMeteo(options, hourly.all())

    # Download data
    meteo = mgr.get_dict()

    match output:
        case "temperature":
            return getHourlyValuesOfDay(meteo, day, "temperature_2m")
        case "felt_temp":
            return getHourlyValuesOfDay(meteo, day, "apparent_temperature")
        case "weathercode":
            l = getHourlyValuesOfDay(meteo, day, output)
            for i, e in enumerate(l):
                l[i] = (e[0], getWeatherCodeString(e[1]))
            return l                
        case _:
            return getHourlyValuesOfDay(meteo, day, output)

# get_weather_forcast(float, float, "YYYY-MM-DD", ["temperatur"/"felt_temp"])

if __name__ == "__main__":
    print(get_weather_forcast(13.7372621, 51.0504088, "2024-05-25", "temperature"))
    print(get_weather_forcast(13.7372621, 51.0504088, "2024-05-25", "weathercode"))