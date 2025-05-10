#Local
from config.logger_config import logger
from utils.decorators import conversionLogger
#Third Party
#Standard Library


@conversionLogger()
def kelvinToFarenheit(kelvin: float):
    """
    Convert Kelvin to Fahrenheit.
    """
    logger.debug(f"Converting {kelvin}K to Fahrenheit")
    if kelvin < 0:
        logger.error("Temperature in Kelvin cannot be negative.")
        raise ValueError("Temperature in Kelvin cannot be negative.")
    return (kelvin - 273.15) * 9/5 + 32


@conversionLogger()
def kelvinToCelsius(kelvin: float):
    """
    Convert Kelvin to Celsius.
    """
    logger.debug(f"Converting {kelvin}K to Celsius")
    if kelvin < 0:
        logger.error("Temperature in Kelvin cannot be negative.")
        raise ValueError("Temperature in Kelvin cannot be negative.")
    return kelvin - 273.15


@conversionLogger()
def CelsiusToFarenheit(celsius: float):
    """
    Convert Celsius to Fahrenheit.
    """
    logger.debug(f"Converting {celsius}C to Fahrenheit")
    if celsius < -273.15:
        logger.error("Temperature in Celsius cannot be below absolute zero.")
        raise ValueError("Temperature in Celsius cannot be below absolute zero.")
    return (celsius * 9/5) + 32


@conversionLogger()
def FarenheitToCelsius(farenheit: float):
    """
    Convert Fahrenheit to Celsius.
    """
    logger.debug(f"Converting {farenheit}F to Celsius")
    if farenheit < -459.67:
        logger.error("Temperature in Fahrenheit cannot be below absolute zero.")
        raise ValueError("Temperature in Fahrenheit cannot be below absolute zero.")
    return (farenheit - 32) * 5/9


@conversionLogger()
def FarenheitToKelvin(farenheit: float):
    """
    Convert Fahrenheit to Kelvin.
    """
    logger.debug(f"Converting {farenheit}F to Kelvin")
    if farenheit < -459.67:
        logger.error("Temperature in Fahrenheit cannot be below absolute zero.")
        raise ValueError("Temperature in Fahrenheit cannot be below absolute zero.")
    return (farenheit - 32) * 5/9 + 273.15


@conversionLogger()
def CelsiusToKelvin(celsius: float):
    """
    Convert Celsius to Kelvin.
    """
    logger.debug(f"Converting {celsius}C to Kelvin")
    if celsius < -273.15:
        logger.error("Temperature in Celsius cannot be below absolute zero.")
        raise ValueError("Temperature in Celsius cannot be below absolute zero.")
    return celsius + 273.15
