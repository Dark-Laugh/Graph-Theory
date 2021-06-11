# -*- coding: utf-8 -*-
"""
Created on Sat May 29 14:59:37 2021

@author: rpthi

Lazy implementation of Dijkstra's inserts duplicate key-value pairs (keys being node index and
value being shortest distance to get to that node) in our PQ because it is more efficient to
insert a new key-value pair in O(log(n)) than it is to update existing key values in O(n)

This is inefficient for dense graphs since we end up with several outdated key-value pairs
in our PQ. The eager version of Dijkstra's avoids duplicates and supports efficient value updates
in O(log(n)) by using an Indexed Priority Queue

Dijkstra's with heaped IPQ: O((E+V)log(V))
[PQDict is heaped]
"""
from pqdict import PQDict

def calculate_distance(adj, node):
    dist = {node: float('infinity') for node in adj}
    dist[node] = 0 # distance from starting node to itself is 0
    prev = {node: None for node in adj}
    ipq = PQDict()
    ipq.additem(node, 0)
    
    while len(ipq) != 0:
        current_node, current_dist = ipq.popitem()
        try: #weird glitch, this fixes it though
            if dist[current_node] < current_dist:
                continue
        except: return dist, prev
        for neighbor, weight in adj[current_node].items():
            distance = current_dist + weight
            if distance < dist[neighbor]:
                prev[neighbor] = current_node
                dist[neighbor] = distance
                if neighbor in ipq: #this is the main difference between lazy and eager
                    ipq.replace_key(neighbor, distance)
                else:
                    ipq.additem(neighbor, distance)

    return dist, prev


#same as lazy
def find_shortest_path(adj, start_node, end_node):
    dist, prev = calculate_distance(adj, start_node)
    path = []
    #base case
    if dist[end_node] == float('infinity'): #means not connected to start_node
        return path
    # start at end_node and go backwards
    # prev[end_node] = temp
    # prev[temp] = temp2 
    # prev[temp2] = temp3    and so on and so forth
    #so, find 'parent' of node, then find 'parent' of parent and so on. Recursion!
    return_path(prev, path, start_node, end_node)
    path = path[::-1] # reverse the list
    return path
    
def return_path(prev, path, start_node, end_node):
        #if node is source aka base case
        #following if statement includes the start and end nodes
        if end_node == None:
            return
        path.append(end_node)
        #print(path)
        return_path(prev, path, end_node, prev[end_node])
        

adj = {
    'U': {'V': 2, 'W': 5, 'X': 1},
    'V': {'U': 2, 'X': 2, 'W': 3},
    'W': {'V': 3, 'U': 5, 'X': 3, 'Y': 1, 'Z': 5},
    'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1},
    'Y': {'X': 1, 'W': 1, 'Z': 1},
    'Z': {'W': 5, 'Y': 1},
    'A': {}
}
#U to Z is 0 to 5
print(find_shortest_path(adj, 'U', 'Z'))