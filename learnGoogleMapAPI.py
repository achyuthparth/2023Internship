import pandas
import requests
# `import googlemaps` is importing the `googlemaps` module, which provides a Python client for the
# Google Maps API. This allows the user to access various methods provided by the API, such as
# geocoding and directions.
import googlemaps

API_KEY = "AIzaSyA1SLSrQuMk74VCC--Nz8ACjBdTJirIej8"

mapClient = googlemaps.Client(API_KEY)

address = '3200 228th Ave SE, Sammamish, WA 98075'
mapClient.geocode(address)
# `geocode` is a method provided by the Google Maps API that takes an address as input and
# returns the corresponding latitude and longitude coordinates of that address.
