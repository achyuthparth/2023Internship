import SingleTspModule
import ClusterGenerator

def travelTime(cluster):
    addressList = []
    for customer in cluster.customerList:
        addressList.append(customer.address)

#def appointmentDuration(cluster)

def clusterCost(cluster = ClusterGenerator.Cluster):
    travelTime = travelTime(cluster)
    #appointmentDuration = appointmentDuration(cluster)
    return travelTime #+ appointmentDuration

def clusterListCost(clusterList):
    sum = 0
    for cluster in clusterList:
        sum += clusterCost(cluster)
    return sum