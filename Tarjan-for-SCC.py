# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 17:20:08 2021

@author: rpthi

SCC (Strongly Connecected Components):
can be thought of as a self-contained cycle within a directed graphg where any vertex
can reach any other vertex in the same cycle.

also, interesting to observe that there is no path from one SCC to another, making a
SCC unique in a graph

recall: low-link value of a node is the smallest [lowest] node id reachable
from that node during a DFS

time complexity: O(V+E)

explanation:
mark id of each node as unvisited, assign id and low-link value
also, mark current nodes as visited and add them to 'seen' stack
on DFS callback, if previous node is on the stack, then min the current node's low-link
value with last node's low link value*
After visiting all neighbors, if current node started a cc**, then pop nodes off stack
until current node is reached
* ie propogation/'continuing' of a low-link value throughout cycles (moves it from prev. to curr.)
** a node started a cc if its id equals its low link value!
since there is no path from one SCC to another, do it again and again

use an adj list but DIRECTED graph, so when we add an edge we only add it once
"""
from collections import defaultdict

class Graph:
    def __init__(self, num_v):
        self.V = num_v
        self.adj = defaultdict(list)
        self.id = 0
    
    def add_edge(self, a, b):
        self.adj[a].append(b)
        
    '''
    node -> vertex to be visited next
    disc[] -> stores discovery id's of visited vertices
    low[] -> low-link value aka earliest possible id reachable by node by whatever path
    stack -> stack of vertices, if part of SCC, pop them. Makes life easy
    stackMember[] -> index array for fast verification whether node is in stack
    '''
    
    def dfs(self, node, low, disc, stackMember, stack):
        # initializing
        disc[node] = self.id
        low[node] = self.id
        self.id += 1
        stackMember[node] = True
        stack.append(node)
        
        # iterate through all neighbors of node
        for neighbor in self.adj[node]:
            # if not visited, dfs it aka recur over it
            if disc[neighbor] == -1:
                self.dfs(neighbor, low, disc, stackMember, stack)
                # Check if the subtree rooted with neighbor has a connection to
                # one of the ancestors of node ie for propogation of low-link value
                # Case 1
                low[node] = min(low[node], low[neighbor])
            
            elif stackMember[neighbor] == True:
                # Case 2
                # update low-link value of node iff neighbor is still in stack
                # uses fact that no SCC can be connected to each other, if it were connected
                # it would still be in stack
                low[node] = min(low[node], disc[neighbor])
        
        w = -1 #stores stack extracted vertices
        if low[node] == disc[node]:
            # then the head/source node has been discovered
            # all nodes on that path are part of SCC, remove from stack etc
            while w != node:
                w = stack.pop()
                print(w)
                stackMember[w] = False

            print("")

            
    def find_SCC(self):
        disc = [-1] * self.V
        low = [-1] * self.V
        stackMember = [False] * self.V
        stack = []
        
        for i in range(self.V):
            if disc[i] == -1:
                self.dfs(i, low, disc, stackMember, stack)
                
g1 = Graph(5)
g1.add_edge(1, 0)
g1.add_edge(0, 2)
g1.add_edge(2, 1)
g1.add_edge(0, 3)
g1.add_edge(3, 4)
print("SSC in graph ")
g1.find_SCC()