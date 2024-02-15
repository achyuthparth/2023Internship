from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from urllib.parse import urlencode
#import googlemaps
import pandas
import requests
import CostFunction

Map_API_KEY = "AIzaSyA1SLSrQuMk74VCC--Nz8ACjBdTJirIej8"

sampleAddressList = ["Lexington, MA, USA", "Cambridge, MA, USA", "Concorde, MA, USA"]
sampleDict = { "startAddress": { "id": 13, "addressLine1": "1600 Amphitheatre Parkway", "addressLine2": "Mountain View", "city": "CA", "state": "US", "zipcode": 94043 }, "addresses": [ { "id": 14, "addressLine1": "1 Infinite Loop", "addressLine2": "Cupertino", "city": "CA", "state": "US", "zipcode": 95014 }, { "id": 15, "addressLine1": "1000 Oracle Parkway", "addressLine2": "Redwood Shores", "city": "CA", "state": "US", "zipcode": 94065 }, { "id": 16, "addressLine1": "6000 Bayfront Expressway", "addressLine2": "San Jose", "city": "CA", "state": "US", "zipcode": 95113 }, { "id": 17, "addressLine1": "101 California Street", "addressLine2": "San Francisco", "city": "CA", "state": "US", "zipcode": 94111 }, { "id": 18, "addressLine1": "701 Van Ness Avenue", "addressLine2": "San Francisco", "city": "CA", "state": "US", "zipcode": 94102 } ] } 
sampleCsv = pandas.read_csv(r"sample.csv")


# get lat and long from an address
def extractLatLong(location, dataType = "json"):
    endpoint = f"https://maps.googleapis.com/maps/api/geocode/{dataType}"
    parameters = {"address": location, "key": Map_API_KEY}
    urlParameters = urlencode(parameters)
    url = f"{endpoint}?{urlParameters}"
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return {}
    latlng = {}
    try:
        latlng = r.json()["results"][0]["geometry"]["location"]
    except:
        pass
    returnDict = latlng.get("lat"), latlng.get("lng")
    return [returnDict[0], returnDict[1]]

# deserialize address list from json
'''
def addressListGen(addressDict = sampleDict):
    '''

# create a pandas data frame of the list of lat and long for all locations
def coordTableGen(addressList = sampleAddressList):
    return pandas.DataFrame([extractLatLong(address) for address in addressList], columns = ["Latitude", "Longitude"])

# generate clusters from the lat/long list
def clusterGen(dataFrame = sampleCsv, agentCount = 2):
    km = KMeans(n_clusters = agentCount)
    predicted = km.fit_predict(dataFrame[["Latitude", "Longitude"]])
    dataFrame["cluster"] = predicted
    return [dataFrame[dataFrame.cluster == i] for i in range(agentCount)]

# maybe create cluster object? attributes: agent loc, centroid, list of customer loc

class Customer:
    def __init__(self, address, duration, latLong):
        self.address = address
        self.duration = duration
        self.latLong = latLong

class Agent:
    def __init__(self, address, latLong):
        self.address = address
        self.latLong = latLong
        
class Cluster:
    def __init__(self, centroid, agent, customerList, clusterCost):
        self.centroid = centroid
        self.agent = agent
        self.customerList = customerList
        self.Cost = clusterCost
    
    def clusterCost(self):
        return CostFunction.clusterCost(self)