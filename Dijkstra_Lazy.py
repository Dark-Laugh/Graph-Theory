# -*- coding: utf-8 -*-
"""
Created on Sat May 29 14:33:04 2021

@author: rpthi

SSSP (Single Source Shortest Path) algorithm for graphs
    means you must specify as starting node for the algorithm

Djikstra's Algorithm is a SSSP algorithm for graphs
with non-negative weights
Time complexity is usually O(E*log(V), competitive against other shortest path algorithms

Explanation:
Maintain a 'dist' (distance) array where the distance to every node is a positive infinity.
Mark the distance to the start node 's' to be 0
Maintain a PQ (Priority Queue) of key-value pairs of (node index,distance) pairs which tell you which node
    to visit next based on sorted min value
Insert (s,0) in to the PQ and loop while PQ is not empty, pulling out the next most promising
    (node index, distance) pair
Iterate over all edges outwards from current node and relax each edge appending a new 
    (node index, distance) key-value pair ot the PQ for every relaxation                             

this implementation of Dijkstra is called lazy because we lazily delete key value pairs
if a better path is present (ie the pair isn't on optimal path)

notice, only returns distances, not path
"""

import heapq
# aka djikstras
def calculate_distances(adj, node): # OPTIMIZATION: stop early by inputting end_node here**
    dist = {node: float('infinity') for node in adj}
    dist[node] = 0 # distance from starting node to itself is 0
    prev = {node: None for node in adj}
    pq = [(node, 0)]
    while len(pq) > 0:
        current_node, current_dist = heapq.heappop(pq)
        # Nodes can get added to the priority queue multiple times. I only
        # process a vertex the first time we remove it from the priority queue.
        if current_dist > dist[current_node]: #neat optimization that ignores 'outdated' nodes
            continue        
        for neighbor, weight in adj[current_node].items():
            distance = current_dist + weight
            # Only consider new path if it's better than one already known (default pos. infinity)
            if distance < dist[neighbor]:
                prev[neighbor] = current_node # index taken to get to neighbor***
                dist[neighbor] = distance
                heapq.heappush(pq, (neighbor, distance))
        # if neighbor == end_node: return dist[e] ** to end distance early, works usually
    return dist, prev
    # *** only space for one though, which is fine since you can see shortest path to get to index
    # and so on and so forth

adj = {
    'U': {'V': 2, 'W': 5, 'X': 1},
    'V': {'U': 2, 'X': 2, 'W': 3},
    'W': {'V': 3, 'U': 5, 'X': 3, 'Y': 1, 'Z': 5},
    'X': {'U': 1, 'V': 2, 'W': 3, 'Y': 1},
    'Y': {'X': 1, 'W': 1, 'Z': 1},
    'Z': {'W': 5, 'Y': 1}
}

def find_shortest_path(adj, start_node, end_node):
    dist, prev = calculate_distances(adj, start_node)
    path = []
    #base case
    if dist[end_node] == float('infinity'): #means not connected t0 start_node
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
        
print(find_shortest_path(adj, 'U', 'Z'))