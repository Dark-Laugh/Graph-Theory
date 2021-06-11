# -*- coding: utf-8 -*-
"""
Created on Fri May 28 14:03:07 2021

@author: rpthi


Explores as fast as possible down a branch before backtracking
O(V+E) time complexity
By itself, not very useful. Only useful when augmented to perform other tasks
e.g. count connected components, determine connectivity, find bridges and/or
articulation points


Plunges depth first, then backtracks and continues
ie 
start at a node, then go through a branch, turning the undirected edges directed,
then backtrack and go through another branch


Here: Normal DFS + finding connected components
other augmentations:
minimum spanning tree
detect and find cycles
check if bipartite
find strongly connected components
topologically sort nodes
find bridges and/or articulation points
find augmenting paths in a flow network
generate mazes
"""


class DepthFirstSearchDIRECTED():
    def __init__(self, adj):
        self.adj = adj #adjacency LIST of graph
        self.visited = set() #visited vertices
    def dfs(self, node):
        if node not in self.visited:
            print(node)
            self.visited.add(node)
            for neighbor in self.adj[node]:
                self.dfs(neighbor)

class DepthFirstSearchUNDIRECTED():
    def __init__(self, adj):
        self.adj = adj #adjacency LIST of graph
        self.visited = set() #visited vertices
        self.component = []
        self.cc = []
        self.count = 0
    
    #to find CC: 
    #find number of connected components given adj LIST
    #do this by labeling each cc as a a different int
    #for all nodes in graph, do dfs.
    #go through all nodes in adj
    def find_cc(self):
          for node in self.adj:
              #print('node' + node)
              if node not in self.visited:
                  self.component = []
                  self.count += 1
                  self.cc.append(self.dfs(node))
          return self.count, self.cc    
                  
    def dfs(self, node):
        self.visited.add(node)
        self.component.append(node)
        for neighbor in self.adj[node]:
            if neighbor not in self.visited:
                self.visited.add(neighbor)
                self.dfs(neighbor) 
        return self.component
'''
graph:
    A
   BC
  DEF
'''   
adj = {
    'A' : ['B','C'],
    'B' : ['D', 'E'],
    'C' : ['F'],
    'D' : [],
    'E' : ['F'],
    'F' : [],
    'G': []
}

#depth_first_search = DepthFirstSearchDIRECTED(adj)
#depth_first_search.dfs('A')

dfsU = DepthFirstSearchUNDIRECTED(adj) #automatically starts at A since it is first in node set
count, cc = dfsU.find_cc()
print(count)
print(cc)