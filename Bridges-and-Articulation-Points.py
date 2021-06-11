# -*- coding: utf-8 -*-
"""
Created on Tue Jun  1 13:26:32 2021

@author: rpthi

A bridge/cut edge is any edge which if removed increases the number of connected
components in a graph.
An articulation point is a vertex/node which if removed increases the number of
connected components in  graph.
These are important concepts as they often hint at bottlenecks/weak points/vulnerabilities

Bridges explanation:
Start at any node and perform a DFS labeling nodes with increasing id values.
Keep track of id, as well as smallest low-link value*. During the DFS, a bridge 
is found when the id of a node an edge is coming from is less than the low link
value of the node the edge is going to.
* low-link value is of a node is the smallest [lowest] id reachable from the node
while doing a DFS, (including itself)
ie, there was no edge connected to the start of the component/back to the component

initialize low-link values as node id,then update as paths to current node are viewed
seems good to have a parent list to keep track of low-link values

Time complexity: if you update the low-link values in one pass: O(V+E)

Observation about articulation points:
if a-b is a bridge, then either a or b is an articulation point. Obvious.
Clearly, this condition alone is insufficient however.
Moreover,
on a callback, if id of (in a-b) a == lowlink of b, then there was a cycle!
The indication of a cycle back to a source node indicates an articulation point
    exception: singleton aka the cycle is the only thing on graph

explanation:
same thing with bridges except we add an ount_edge_count aka 'child' count

recall: u is an articulation point in following cases
(1) u is root of DFS tree and has two or more chilren.  (CYCLE)
(2) If u is not root and low value of one of its child is more than discovery value of u.
    (IS THE ART.POINT OF BRIDGE)
"""

#it always seems better to initialize graph and add edges
#then, either use edge list or adjacency matrix
from collections import defaultdict

class Graph:
    def __init__(self, num_v):
        self.V = num_v
        self.adj = defaultdict(list)
        self.id = 0
        self.bridges = []
        self.ap = []
    
    def add_edge(self, a, b):
        self.bridges = []
        self.ap = []
        self.adj[a].append(b)
        self.adj[b].append(a)
    
    '''
    node: to be visited
    visited: array of visited nodes
    parent: array of DFS trees
    disc: array of discovery id's of visited vertices
    '''
    def dfs_b(self,node,visited,parent,low,disc):
        #current node is visited
        visited[node] = True
        #initialize discovery id and low value
        disc[node] = self.id
        low[node] = self.id
        self.id += 1
        #iterate over all neighbors to node
        for neighbor in self.adj[node]:
            #if it's not visited, make it a child of node in a DFS tree and iterate for it
            if visited[neighbor] == False:
                parent[neighbor] = node
                self.dfs_b(neighbor, visited, parent, low, disc)
                #check if subtree with neighbor as root has a connection to a parent of node
                #if so, then match low-link value
                low[node] = min(low[node], low[neighbor])
                '''
                if the lowest vertex reachable from subtree under neighbor is below node, then
                node-neighbor is a bridge
                ie
                if the low-link of neighbor is greater than the id of node, bridge
                ie
                there was no edge connecting neighbor to an ancestor of node (somewhere in the
                                                                              CC)
                '''
                if low[neighbor] > disc[node]:
                    self.bridges.append(node)
                    self.bridges.append(neighbor)
                    print("%d %d"%(node,neighbor))
            
            elif neighbor != parent[node]: #update low-value
                low[node] = min(low[node], disc[neighbor])
        
    def find_bridges(self):
        self.id = 0
        self.bridges = []
        #initialize vertices to not visited
        #           and all arrays
        visited = [False] * self.V
        disc = [float("Infinity")] * (self.V)
        low = [float("Infinity")] * (self.V)
        parent = [-1] * (self.V)
        #call the recursive dfs to find bridges
        for i in range(self.V):
            if visited[i] == False:
                self.dfs_b(i, visited, parent, low, disc)


    #ap[] articulation poitns
    def dfs_a(self,node,visited,parent,low,disc):
        #the only difference here is the 'child' variable
        out_edge = 0
        visited[node] = True
        disc[node] = self.id
        low[node] = self.id
        self.id += 1
        #iterate for all neighbors of node
        for neighbor in self.adj[node]:
            #if neighbor isn't visited yet, make it a child of node, and increase node's
            #out_edges aka child count
            if visited[neighbor] == False:
                parent[neighbor] = node
                out_edge += 1
                self.dfs_a(neighbor, visited, parent, low, disc)
                low[node] = min(low[node], low[neighbor])
                
                #node is an articulation point if
                #(1) node is root of dfs tree and had >= 2 children
                if parent[node] == -1 and out_edge >= 2:
                    self.ap.append(node)
                    print("%d"%(node))
                
                #(2) If node isn't a root and low value of one of its child is more
                # than discovery value of u.
                if parent[node] != -1 and low[neighbor] >= disc[node]:
                    self.ap.append(node)
                    print("%d"%(node))

            elif neighbor != parent[node]: #update low-value
                low[node] = min(low[node], disc[neighbor])
                
                
    def find_articulation_points(self):
        self.id = 0
        self.ap = []
        visited = [False] * self.V
        disc = [float("Infinity")] * (self.V)
        low = [float("Infinity")] * (self.V)
        parent = [-1] * (self.V)
        
        #call the recursive dfs to find bridges
        for i in range(self.V):
            if visited[i] == False:
                self.dfs_a(i, visited, parent, low, disc)




g1 = Graph(5)
g1.add_edge(1, 0)
g1.add_edge(0, 2)
g1.add_edge(2, 1)
g1.add_edge(0, 3)
g1.add_edge(3, 4)
  
   
print("Bridges in graph ")
g1.find_bridges()
print("Articulation points in graph ")
g1.find_articulation_points()
        