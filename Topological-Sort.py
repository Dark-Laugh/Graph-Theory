# -*- coding: utf-8 -*-
"""
Created on Fri May 28 16:40:25 2021

@author: rpthi

Motivation:
Many real world applications can be modeled as graphs with directed edges where
some events must happen before others:
eg school class prerequisites, program dependencies, event scheduling etc.

so,
gives topological ordering on a directed acyclic graph (DAG) and the algorithm is
O(V+E) time
[obviously acyclic as if cyclic then invalid dependency since you have no valid place to start and end]

Note: topological orderings are NOT unique

Q: How do I verify that my graph contains no cyclic?
A: One method is Tarjan's strongly cc algorithm which can be used to find cycles

By definition all trees have topological orderings. Finding the TO is easy if tree
since you can just cherry-pick from the bottom

How it works:
pick acyclic node
do a DFS exploring only unvisited nodes
on recursive callback of DFS, add current node to to topoogical ordering in reverse order
    ie once you reach the end, add that node to the back of the list ie could use a stack
        OR, put it in a list, then reverse the list. THIS IS WHAT I WILL DO

EXAMPLE
'A' : ['B','C'],
'B' : ['D', 'E'],
'C' : ['F'],
'D' : [],
'E' : ['F'],
'F' : [],
    
graph:
    A
   BC
  DEF

A to B to D      so D is in list
     B to E to F      so F is in list
          E to F     so E is in list (F already there)
     B is in list (nowhere else to go)
          
     C to F     so C is in list (F already there)
     C is in list(nowhere else to go)  
A is in list (nowhere else to go)
now reverse the list or make it a stack
"""
#adj is adjacency LIST
def TS(adj):
    visited = []
    for node in adj:
        if node not in visited:
            visitedNodes = []
            visitedNodes = dfs(adj, visitedNodes, node)
            '''
            visited nodes in the path of nodes, the first is the root of the path
            hence it should be last in list, but here it is first (and the only one added) since
            the list will be reversed
            **output if visited.append(visitedNodes) is
            [['F'], ['E', 'F'], ['D'], ['C', 'F'], ['B', 'D', 'E', 'F'], ['A', 'B', 'D', 'E', 'F', 'C']]
            notice, the first node in the above list is correct
            **outpt if visited.append(visitedNodes[0]) is
            ['F', 'E', 'D', 'C', 'B', 'A']
            
            '''
            visited.append(visitedNodes[0])
    return visited[::-1]      
            
def dfs(adj, visitedNodes, node):
    if node not in visitedNodes:
        visitedNodes.append(node)
        for neighbor in adj[node]:
            dfs(adj, visitedNodes, neighbor)
    return visitedNodes
#is O(V+E) since I pass the visitedNodes list so it's returning a full branch at a time

adj = {
    'A' : ['B','C'],
    'B' : ['D', 'E'],
    'C' : ['F'],
    'D' : [],
    'E' : ['F'],
    'F' : [],
}
#expected output is something like: F,E,D,B,C,A or F,E,D,C,B,A
topologically_sorted = TS(adj)
print(topologically_sorted)