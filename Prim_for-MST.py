# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:41:43 2021

@author: rpthi

Minimum Spanning Tree:
    Given an undirected graph, a MST is a subset of the edges in the graph
    which connects all vertices in the graph (without creating cycles) while
    minimizing the total edge cost
    Note: all nodes must be connected to form a MST
    
Prim's is a greedy MST algorithm that performs better on dense graphs than its
rivals eg Kruskal's and Boruvka's. However, when it comes to disconnected graphs,
Prim's cannot do this easily, the algorithm must be performed on each cc, seperately.

Lazy version of Prim's has runtime of O(E * log(E))

Overview of Lazy:
Maintain a min PriorityQueue (PQ) that sorts edges based on min cost. This will
be used to determine the next node to visit and the edge used to get there.
Start on node S. Mark S as visited and iterate over all edges of S, adding them
to PQ. While PQ not empty, and an MST not formed, dequeue the next cheapest edge
from the PQ. If the the dequeued edge is outdated (node it goes to is visited already),
then skip it and poll again. Otherwise, mark the current node as visited and add
the selected edge to the MST. Iterate over the new current node's edges and all
edges to PQ. Do not add edges to PQ which point to an already visited node.
We know the MST is complete when the number of edges is once less than number of nodes
(ie the definition of a tree!)
Note: An adj list representation stores each undirected edge as two directed edges

lazy inserts up to E edges into the PQ, hence, each poll operation on PQ is 
O(log(E)). Instead of blindly inserting edges into a PQ which could later become
stale, the eager version of Prim's tracks (node, edge) key-value pairs that can 
easily be updated and polled to determine the next best edge to add to MST.

Realization: 
An MST is a directed tree. Further, each node is paired with exactly one
of its incoming edges (exception: start node). This can easily be seen on a directed MST
where you can have multiple edges leaving a node, but at most one edge entering a node.

In the Eager version, we are trying to determine which of a node's incoming edges to
select to include in the MST (all nodes must be included, so we decide which edge for each node)
A slight difference from the lazy version is instead of of adding edges to the PQ as we iterate
over the edges of a node, we're going to relax (update) the destination node's most promising
incoming edge.
A natural question: How to efficiently update and retrieve these (node, edge) pairs?
A solution: Indexed Priortity Queue which can efficiently update and poll pairs. 
This reduces time complexity from O(E * logE) to O(E * logV) since there can only
be V (node, edge) pairs in the IPQ, making the update and poll functions O(logV)

Overview of Eager:
    
Maintain a min IPQ of size V that sorts vertex-edge pairs (v,e) based on min cost
of e. By default, all vertices v have best value of (v,infinity) in the IPQ.
Start algorithm at any node. Mark node as visited and *relax all edges of node.
While IPQ is nonempty and no MST has been formed, dequeue the next best (v,e) pair
from the IPQ. Mark node v as visited and add edge e to the MST. Next, relax all edges
of v while making sure not to relax any edge pointing to a node already visited.

* in this instance, relax refers to updating the entry for node v in IPQ from
(v, e_old) to (v, e_new) if lower cost, obviously.

note: if node to node has cheaper path going through another node, we update that as well
    e.g. going from 0 to 5 has cost 7, but going from 0 to 2 to 5 has cost 6, then
    update 0 to 5 as having cost 6


"""
from collections import defaultdict
import heapq

class Graph:
    def __init__(self, num_v):
        self.V = num_v
        self.adj = defaultdict(list) # adj list, for especially dense graphs, use a matrix
    
    def addEdge(self, a, b, weight):
        self.adj[a].append((b,weight))
        self.adj[b].append((a,weight))
        
        
    # O(E*logV) function
    # correct cost, now path?
    def eager_prim(self):
        start = mstCost = 0
        visited = {start}
        minHeap = []
        mst = {start}
        for neighbor, weight in self.adj[start]:
            heapq.heappush(minHeap,(neighbor, weight))
        while len(visited) < self.V + 1 and minHeap:
            next_node, cost = heapq.heappop(minHeap)
            if next_node not in visited:
                visited.add(next_node)
                mstCost += cost
                mst.add(next_node)
                for next_, next_cost in self.adj[next_node]:
                    if next_ not in visited:
                        heapq.heappush(minHeap, (next_, next_cost))
        return mstCost
      

graph = Graph(9)
graph.addEdge(0, 1, 4)
graph.addEdge(0, 7, 8)
graph.addEdge(1, 2, 8)
graph.addEdge(1, 7, 11)
graph.addEdge(2, 3, 7)
graph.addEdge(2, 8, 2)
graph.addEdge(2, 5, 4)
graph.addEdge(3, 4, 9)
graph.addEdge(3, 5, 14)
graph.addEdge(4, 5, 10)
graph.addEdge(5, 6, 2)
graph.addEdge(6, 7, 1)
graph.addEdge(6, 8, 6)
graph.addEdge(7, 8, 7)
mstCost = graph.eager_prim()
print(mstCost)
