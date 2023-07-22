from googlemaps import distance_matrix
import requests
import json

API_KEY = "AIzaSyA1SLSrQuMk74VCC--Nz8ACjBdTJirIej8"


url = f"https://maps.googleapis.com/maps/api/distancematrix/json?"
def AddressQueryList(addressList):
    queryList = ""
    for addy in addressList:
        string = "".join(f"{i}+" for i in addy.split(","))
        string = (string[:-1]).replace(" ","")
        queryList += f"{string}|"
    return queryList[:-1]
    
def getJson(agentLoc, addressList):
    if addressList is None:
        addressList = []
    destinations = AddressQueryList(addressList)
    newAddressList = addressList.append(agentLoc)
    origins = AddressQueryList(newAddressList)
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={destinations}&departure_time=now&key={API_KEY}"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text

print(getJson("22772 SE 32nd St Sammamish WA", [ "Lexington, MA, USA", "Concord, MA, USA" ]))

