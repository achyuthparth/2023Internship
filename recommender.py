import SingleTspModule
import CostFunction

# deserialize json into a csv for convenience

# k-means cluster to assign customer to agent based on proximity

# cost function -> cost = travel time + aggregate appointment time

# travel time calculator

# appointment time calculator

# aggregate appointment time calculator

# forward shuffler algorithm
'''
calculate cost functions for both clusters and reassign ordering
move closest appointment to cluster1 from cluster2 to cluster1
    if cost is more: call with next cluster
    else call same function with same clusters but with new added appointments
'''
# backward shuffler algorithm

'''calculate cost functions for both clusters and reassign ordering
move closest appointment to cluster N from cluster N-1 to cluster N
    if cost is more: call with previous cluster
    else call same function with same clusters but with new added appointments'''
    
