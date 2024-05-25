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
        res.append((meteo["hourly"][valuelist][i], meteo["hourly"]["time"][i]))
    return res


def getHourlyValuesOfDay(meteo: dict, day: str, output: str) -> list:
    return getListFromIndex(meteo, output, indexesfromregex(meteo["hourly"]["time"], day + "T[0-3][0-9]:00"))


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
        case _:
            return getHourlyValuesOfDay(meteo, day, output)

# get_weather_forcast(float, float, "YYYY-MM-DD", ["temperatur"/"felt_temp"])