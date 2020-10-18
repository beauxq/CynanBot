import math
from typing import List


class WeatherReport():

    def __init__(
        self,
        airQuality: int,
        humidity: float,
        pressure: float,
        temperature: float,
        tomorrowsHighTemperature: float,
        tomorrowsLowTemperature: float,
        alerts: List[str],
        conditions: List[str],
        tomorrowsConditions: List[str]
    ):
        if humidity == None or not math.isfinite(humidity):
            raise ValueError(f'humidity argument is malformed: \"{humidity}\"')
        elif pressure == None or not math.isfinite(pressure):
            raise ValueError(f'pressure argument is malformed: \"{pressure}\"')
        elif temperature == None or not math.isfinite(temperature):
            raise ValueError(f'temperature argument is malformed: \"{temperature}\"')
        elif tomorrowsHighTemperature == None or not math.isfinite(tomorrowsHighTemperature):
            raise ValueError(f'tomorrowsHighTemperature argument is malformed: \"{tomorrowsHighTemperature}\"')
        elif tomorrowsLowTemperature == None or not math.isfinite(tomorrowsLowTemperature):
            raise ValueError(f'tomorrowsLowTemperature argument is malformed: \"{tomorrowsLowTemperature}\"')

        self.__airQuality = airQuality
        self.__humidity = int(round(humidity))
        self.__pressure = int(round(pressure))
        self.__temperature = temperature
        self.__tomorrowsHighTemperature = tomorrowsHighTemperature
        self.__tomorrowsLowTemperature = tomorrowsLowTemperature
        self.__alerts = alerts
        self.__conditions = conditions
        self.__tomorrowsConditions = tomorrowsConditions

    def __cToF(self, celsius: float):
        return (celsius * (9 / 5)) + 32

    def getAirQuality(self):
        return self.__airQuality

    def getAlerts(self):
        return self.__alerts

    def getConditions(self):
        return self.__conditions

    def getHumidity(self):
        return self.__humidity

    def getPressure(self):
        return self.__pressure

    def getTemperature(self):
        return int(round(self.__temperature))

    def getTemperatureImperial(self):
        return int(round(self.__cToF(self.__temperature)))

    def getTomorrowsConditions(self):
        return self.__tomorrowsConditions

    def getTomorrowsLowTemperature(self):
        return int(round(self.__tomorrowsLowTemperature))

    def getTomorrowsLowTemperatureImperial(self):
        return int(round(self.__cToF(self.__tomorrowsLowTemperature)))

    def getTomorrowsHighTemperature(self):
        return int(round(self.__tomorrowsHighTemperature))

    def getTomorrowsHighTemperatureImperial(self):
        return int(round(self.__cToF(self.__tomorrowsHighTemperature)))

    def hasAirQuality(self):
        return self.__airQuality != None

    def hasAlerts(self):
        return self.__alerts != None and len(self.__alerts) >= 1

    def hasConditions(self):
        return self.__conditions != None and len(self.__conditions) >= 1

    def hasTomorrowsConditions(self):
        return self.__tomorrowsConditions != None and len(self.__tomorrowsConditions) >= 1
