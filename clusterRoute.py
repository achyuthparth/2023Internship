import json 
import numpy as np
import requests
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

#sampleDict = { "startAddress": { "id": 13, "addressLine1": "1600 Amphitheatre Parkway", "addressLine2": "Mountain View", "city": "CA", "state": "US", "zipcode": 94043 }, "addresses": [ { "id": 14, "addressLine1": "1 Infinite Loop", "addressLine2": "Cupertino", "city": "CA", "state": "US", "zipcode": 95014 }, { "id": 15, "addressLine1": "1000 Oracle Parkway", "addressLine2": "Redwood Shores", "city": "CA", "state": "US", "zipcode": 94065 }, { "id": 16, "addressLine1": "6000 Bayfront Expressway", "addressLine2": "San Jose", "city": "CA", "state": "US", "zipcode": 95113 }, { "id": 17, "addressLine1": "101 California Street", "addressLine2": "San Francisco", "city": "CA", "state": "US", "zipcode": 94111 }, { "id": 18, "addressLine1": "701 Van Ness Avenue", "addressLine2": "San Francisco", "city": "CA", "state": "US", "zipcode": 94102 } ] } 

API_KEY = "AIzaSyA1SLSrQuMk74VCC--Nz8ACjBdTJirIej8"
data = None
manager = None
routing = None

def createURL(addressList = []):
    queryList = ""
    for addy in addressList:
        string = "".join(f"{i}+" for i in addy.split(","))
        string = (string[:-1]).replace(" ","")
        queryList += f"{string}|"
    queryList = queryList[:-1]

    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={queryList}&destinations={queryList}&departure_time=now&key={API_KEY}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def createDistanceMatrix(addressList = []):
    loadJson = createURL(addressList)
    
    data = loadJson["rows"]
    times = np.zeros(shape=(len(data), len(data)))
    for i, element in enumerate(data):
        for j, unit in enumerate(element["elements"]):
            duration = unit["duration"]
            value = duration["value"]
            times[i][j] = value
    return (times)

def create_data_model(addressList=None):
    if addressList is None:
        addressList = [[]]
    distanceMatrix = createDistanceMatrix(addressList)
    return {"distance_matrix": distanceMatrix, "num_vehicles": 1, "depot": 0, }


def distance_callback(from_index, to_index):
    fromNode = manager.IndexToNode(from_index)
    toNode = manager.IndexToNode(to_index)
    return data['distance_matrix'][fromNode][toNode]


def print_solution(manager, routing, solution):
    #print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = []
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output.append(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output.append(manager.IndexToNode(index))
    return (plan_output)
    #plan_output += 'Route distance: {}miles\n'.format(route_distance)

    
def clusterRoute(addressList=None):
    if addressList is None:
        addressList = ["Lexington, MA, USA", "Cambridge, MA, USA", "Concorde, MA, USA"]
    global data
    global manager
    global routing
    data = create_data_model(addressList)
    manager = pywrapcp.RoutingIndexManager(len(data["distance_matrix"]), data["num_vehicles"], data["depot"])
    routing = pywrapcp.RoutingModel(manager)

    callbackIndex = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(callbackIndex)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)
    if solution:
        returnList = print_solution(manager = manager, routing = routing, solution = solution)

    returnDict = {}
    returnDict["Order"] = []
    for k,element in enumerate(returnList):
        if k > 0:
            time = data["distance_matrix"][k - 1][k - 2]
        else: time = data["distance_matrix"][0][0]
        returnDict["Order"].append({"ID": returnList[k], "Time": time})
    return returnDict


print(clusterRoute())