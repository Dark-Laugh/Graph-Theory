# -*- coding: utf-8 -*-
"""
Created on Fri May 28 16:21:59 2021

@author: rpthi

particularly useful for one thing: finding shortest path on unweighted graphs
time complexity: O(V+E)
usually a building block

how it works:
works in levels/layers
considers neighbors ie explores nodeA, then nodeA's neighbors called next-level
so, explores nodes in layers at a time
this can be done with a queue
see all of nodeA's neighbors and add them to the queue, go to them all and add all their neighbors to the queue
due to how a queue functions, this works well; ie add them to list


GRID:
motivation:
grids are a form of implicit graph as we can determine a node's neighbors based on
location in grid

common way of solving grid problems is to convert to a familiar format e.g. adj list
important: unweighted and grid cells ie nodes connect up,down,left,right
First label the grids in cells w/ ints [0, n) where n = #rows*#columns

Direction vectors
[-1,0]:left,[1,0]:right,[0,-1]:down,[0,1]:up
so, establish vectors, then constraints (ie don't exit screen)
find shortest path between 2 cells.
https://www.youtube.com/watch?v=09_LlHjoEiY ~50 minutes in
"""

class BFS():
    def __init__(self, adj):
        self.adj = adj
        self.visited = []
        self.queue = []

    def bfs(self, node):
        self.visited.append(node)
        self.queue.append(node)
        
        while self.queue:
            v = self.queue.pop(0)
            print(v, end=' ')
            
            for neighbor in self.adj[v]:
                if neighbor not in self.visited:
                    self.visited.append(neighbor)
                    self.queue.append(neighbor)

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

breadth_first_search = BFS(adj)
breadth_first_search.bfs('A')