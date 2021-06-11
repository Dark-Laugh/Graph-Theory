# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 13:21:53 2021

@author: rpthi

An Eulerian path/trail is a path of edges that visits all the edges in a graph
at least once
Note: not every graph has one, and you have to be careful where you start since
    choosing the wrong starting node can lead to unreachable edges
    
An Eulerian circuit is a Eulerian path that starts and ends on the same vertex

Conditions required for valid Eulerian path or Eulerian Circuit:
    
Undirected graph: Complexity of O(V+E)
    Circuit: Every vertex has even degree
    Path: Either every vertex has even degree or exactly or exactly
            two vertices have odd degree
Directed Graph:
    Circuit: Every vertex has equal indegree and outdegree
    Path: At most one vertex has outdegree-indegree=1 and at most one vertex
        has indegree-outdegree=1 and all other vertices have equal in and out
        degrees

Explanation for Undirected Graph:
So, we just need to check the above conditions.
So, all we need to do is make sure all nodes of degree not equaling zero
are connected. We can do this easily with a DFS visiting. Then, check conditions.

Explanation for Directed Graph:
So, we just need to check the above conditions.
For a Eulerian circuit, we can reword the condition to mean if all vertices with
nonzero degre belong to a single strongly connected component


"""
from collections import defaultdict

class UnDirectedGraph:
    def __init__(self, num_v):
        self.V = num_v
        self.adj = defaultdict(list) # I will do an adj list
        
    def add_edge(self,a,b):
        self.adj[a].append(b)
        self.adj[b].append(a)
    
    # outputs:   
    # 0 -> graph has no eulerian path or ciruit
    # 1 -> graph is semi-eulerian ie has eulerian path
    # 2 -> graph is eulerian ie has eulerian circuit
    def is_eulerian(self):    
        # check if all vertexes with non-zero degree are connected
        if self.is_connected() == False:
            return 0
        else:
            '''Recall conditions for Eulerian stuff in undirected graph:
                Circuit: Every vertex has even degree
                Path: Either every vertex has even degree or exactly or EXACTLY
                    two vertices have odd degree
                So, we count number of vertices with odd degree
            '''
            odd = 0
            for node in range(self.V):
                if len(self.adj[node]) % 2 != 0:
                    odd += 1
            
            if odd == 0:
                return 2
            elif odd == 2:
                return 1
            else:
                return 0

    def is_connected(self):
        # intialize all vertices as non-visited
        visited = [False] * self.V
        # Find a vertex/node with non-zero degree
        for node in range(self.V):
            if len(self.adj[node]) > 1:
                break
        # Exception case: No edges in graph so technically connected
        if node == self.V-1:
            return True
         
        # Start dfs with a node of non-zero degree
        self.dfs(node, visited)
        
        # Assert all non-zero degrees are visited
        # If not, it means that there exist unreachable edges
        for i in range(self.V):
            if visited[i] == False and len(self.adj[i]) > 0:
                return False
        
        
        return True
            
    def dfs(self, node, visited):
        # Current node is visited
        visited[node] = True
        for neighbor in self.adj[node]:
            if visited[neighbor] == False:
                self.dfs(neighbor, visited)
        
        
class DirectedGraph:
    def __init__(self, num_v):
        self.V = num_v
        self.adj = defaultdict(list) # I will do an adj list
        
    def add_edge(self,a,b):
        self.adj[a].append(b)
        self.adj[b].append(a)
        
        
    

