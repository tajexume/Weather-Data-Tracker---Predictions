import utils.collector as collector
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('--city', help='City name')
@click.option('--country', default='', help='Country code')
@click.option('--latitude', '--lat', type=float, default=0.0, help='Latitude of the city')
@click.option('--longitude', '--lon', type=float, default=0.0, help='Longitude of the city')
def currentWeather(city, country, latitude, longitude):
    "Get current weather information and add to database"
    if city and not country:
        lat, lon = collector.getCoordinates(city)
        weatherInfo = collector.getCurrentWeather(lat, lon)
        collector.addCurrentWeatherToDB(weatherInfo)
    elif city and country:
        lat, lon = collector.getCoordinates(city, country)
        weatherInfo = collector.getCurrentWeather(lat, lon)
        collector.addCurrentWeatherToDB(weatherInfo)
    elif latitude and longitude:
        weatherInfo = collector.getCurrentWeather(latitude, longitude)
        collector.addCurrentWeatherToDB(weatherInfo)
    else:
        click.echo("Please provide either city, city and country, or latitude and longitude.")
        return

@cli.command()
def version():
    click.echo("0.1.0")

if __name__ == '__main__':
    cli()
