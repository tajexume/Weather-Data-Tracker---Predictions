#! /bin/bash

source .venv/bin/activate
while IFS= read -r city || [ -n "$city" ]; do
  echo "Processing city: $city"
  python3 -m weather_cli currentweather --city "$city"
  # Put your command here, e.g.:
  # python3 weather_cli.py --city "$city"
done < cities.txt
