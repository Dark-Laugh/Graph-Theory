# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 11:07:53 2021

@author: rpthi

Suppose each edge in a graph has maximum capacity which cannot be exceeded.
There is a source and a sink node. 
Motivation/Question: With an infinite source, how much 'flow' can we push
                     through the network given each edge's capacities
Effectively, flow value is th 'bottleneck' value for the amount of flow that can
pass through the network from source to sink under all constrains

Dinic's Algorithm:
Strongly polynomical maximum flow algorithm with runtime of O(E*V^2). However,
on bipartite graphs it has runtime of O(EV^1/2).
Idea: to guide augmenting paths from s -> t using a level graph ie always progressing
'towards' the general direction of the sink in levels.
Levels of graph are obtained from BFS from the source. Edge is only part of level graph
if it makes 'progress' towards the sink. Edges not going 'towards' sink are to be taken
as a detour iff necessary. 
1: Construct level graph with BFS
2: If sink not reached during building of level graph, stop and return max flow
3: Using only valid edges in level graph, perform multiple DFSs from S -> T until
   a blocking flow is reached. Sum over bottleneck values of all augmenting paths
   to calculate max flow.
REPEAT

"""
from collections import defaultdict
class Dinic: 
    def __init__(self, num_v):
        self.lvl = [0] * num_v # level
        self.ptr = [0] * num_v # start | residual edge?
        self.q = [0] * num_v # augmenting path
        self.adj = defaultdict(list)
    # vertex closest to source, vertex closest to sink and flow capacity
    # through that edge, residual edge capacity
    def add_edge(self, a, b, c, rcap=0):
        self.adj[a].append([b, len(self.adj[b]), c, 0])
        self.adj[b].append([a, len(self.adj[a])-1, rcap, 0])
        
    # calculate flow that reaches sink
    def max_flow(self, source, sink):
        flow =  0
        self.q[0] = source
        for l in range(31):  # noqa: E741  l = 30 maybe faster for random data
            while True:
                self.lvl = [0] * len(self.q)
                self.ptr = [0] * len(self.q)
                qi = 0
                qe = 1
                self.lvl[source] = 1
                while qi < qe and not self.lvl[sink]:
                    node = self.q[qi]
                    qi += 1
                    for edge in self.adj[node]:
                        if not self.lvl[edge[0]] and (edge[2] - edge[3]) >> (30 - l):
                            self.q[qe] = edge[0]
                            qe += 1
                            self.lvl[edge[0]] = self.lvl[node] + 1
                p = self.dfs(source, sink, float('inf'))
                while p:
                    flow += p
                    p = self.dfs(source, sink, float('inf'))
                
                if not self.lvl[sink]:
                    break
        return flow
    
    def dfs(self, node, sink, flow):
        if node == sink or not flow:
            return flow
        # start: self.ptr[node]; stop: len(self.adj[node])
        # goes through 
        for i in range(self.ptr[node], len(self.adj[node])):
            edge = self.adj[node][i]
            if self.lvl[edge[0]] == self.lvl[node] + 1:
                p = self.dfs(edge[0], sink, min(flow, edge[2]-edge[3]))
                if p:
                    self.adj[node][i][3] += p
                    self.adj[edge[0]][edge[1]][3] -= p
                    return p
            self.ptr[node] = self.ptr[node] + 1
        return 0


# Here we make a graphs with 10 vertex(source and sink includes)
graph = Dinic(10)
source = 0
sink = 9
"""
Now we add the vertices next to the font in the font with 1 capacity in this edge
(source -> source vertices)
"""
for vertex in range(1, 5):
    graph.add_edge(source, vertex, 1)
"""
We will do the same thing for the vertices near the sink, but from vertex to sink
(sink vertices -> sink)
"""
for vertex in range(5, 9):
    graph.add_edge(vertex, sink, 1)
"""
Finally we add the verices near the sink to the vertices near the source.
(source vertices -> sink vertices)
"""
for vertex in range(1, 5):
    graph.add_edge(vertex, vertex + 4, 1)
 
# Now we can know what the maximum flow(source -> sink) is
print(graph.max_flow(source, sink))

'''-----------------------------------------------------------------------------
Edmonds-Karp: Nearly identical to Ford-Fulkerson

'''
class FlowNetwork:
    def __init__(self, graph, sources, sinks):
        self.sourceIndex = None
        self.sinkIndex = None
        self.graph = graph
 
        self._normalizeGraph(sources, sinks)
        self.verticesCount = len(graph)
        self.maximumFlowAlgorithm = None
 
    # make only one source and one sink
    def _normalizeGraph(self, sources, sinks):
        if sources is int:
            sources = [sources]
        if sinks is int:
            sinks = [sinks]
 
        if len(sources) == 0 or len(sinks) == 0:
            return
 
        self.sourceIndex = sources[0]
        self.sinkIndex = sinks[0]
 
        # make fake vertex if there are more
        # than one source or sink
        if len(sources) > 1 or len(sinks) > 1:
            maxInputFlow = 0
            for i in sources:
                maxInputFlow += sum(self.graph[i])
 
            size = len(self.graph) + 1
            for room in self.graph:
                room.insert(0, 0)
            self.graph.insert(0, [0] * size)
            for i in sources:
                self.graph[0][i + 1] = maxInputFlow
            self.sourceIndex = 0
 
            size = len(self.graph) + 1
            for room in self.graph:
                room.append(0)
            self.graph.append([0] * size)
            for i in sinks:
                self.graph[i + 1][size - 1] = maxInputFlow
            self.sinkIndex = size - 1
 
    def findMaximumFlow(self):
        if self.maximumFlowAlgorithm is None:
            raise Exception("You need to set maximum flow algorithm before.")
        if self.sourceIndex is None or self.sinkIndex is None:
            return 0
 
        self.maximumFlowAlgorithm.execute()
        return self.maximumFlowAlgorithm.getMaximumFlow()
 
    def setMaximumFlowAlgorithm(self, Algorithm):
        self.maximumFlowAlgorithm = Algorithm(self)
 
 
class FlowNetworkAlgorithmExecutor:
    def __init__(self, flowNetwork):
        self.flowNetwork = flowNetwork
        self.verticesCount = flowNetwork.verticesCount
        self.sourceIndex = flowNetwork.sourceIndex
        self.sinkIndex = flowNetwork.sinkIndex
        # it's just a reference, so you shouldn't change
        # it in your algorithms, use deep copy before doing that
        self.graph = flowNetwork.graph
        self.executed = False
 
    def execute(self):
        if not self.executed:
            self._algorithm()
            self.executed = True
 
    # You should override it
    def _algorithm(self):
        pass
 
 
class MaximumFlowAlgorithmExecutor(FlowNetworkAlgorithmExecutor):
    def __init__(self, flowNetwork):
        super().__init__(flowNetwork)
        # use this to save your result
        self.maximumFlow = -1
 
    def getMaximumFlow(self):
        if not self.executed:
            raise Exception("You should execute algorithm before using its result!")
 
        return self.maximumFlow
 
 
class PushRelabelExecutor(MaximumFlowAlgorithmExecutor):
    def __init__(self, flowNetwork):
        super().__init__(flowNetwork)
 
        self.preflow = [[0] * self.verticesCount for i in range(self.verticesCount)]
 
        self.heights = [0] * self.verticesCount
        self.excesses = [0] * self.verticesCount
 
    def _algorithm(self):
        self.heights[self.sourceIndex] = self.verticesCount
 
        # push some substance to graph
        for nextVertexIndex, bandwidth in enumerate(self.graph[self.sourceIndex]):
            self.preflow[self.sourceIndex][nextVertexIndex] += bandwidth
            self.preflow[nextVertexIndex][self.sourceIndex] -= bandwidth
            self.excesses[nextVertexIndex] += bandwidth
 
        # Relabel-to-front selection rule
        verticesList = [
            i
            for i in range(self.verticesCount)
            if i != self.sourceIndex and i != self.sinkIndex
        ]
 
        # move through list
        i = 0
        while i < len(verticesList):
            vertexIndex = verticesList[i]
            previousHeight = self.heights[vertexIndex]
            self.processVertex(vertexIndex)
            if self.heights[vertexIndex] > previousHeight:
                # if it was relabeled, swap elements
                # and start from 0 index
                verticesList.insert(0, verticesList.pop(i))
                i = 0
            else:
                i += 1
 
        self.maximumFlow = sum(self.preflow[self.sourceIndex])
 
    def processVertex(self, vertexIndex):
        while self.excesses[vertexIndex] > 0:
            for neighbourIndex in range(self.verticesCount):
                # if it's neighbour and current vertex is higher
                if (
                    self.graph[vertexIndex][neighbourIndex]
                    - self.preflow[vertexIndex][neighbourIndex]
                    > 0
                    and self.heights[vertexIndex] > self.heights[neighbourIndex]
                ):
                    self.push(vertexIndex, neighbourIndex)
 
            self.relabel(vertexIndex)
 
    def push(self, fromIndex, toIndex):
        preflowDelta = min(
            self.excesses[fromIndex],
            self.graph[fromIndex][toIndex] - self.preflow[fromIndex][toIndex],
        )
        self.preflow[fromIndex][toIndex] += preflowDelta
        self.preflow[toIndex][fromIndex] -= preflowDelta
        self.excesses[fromIndex] -= preflowDelta
        self.excesses[toIndex] += preflowDelta
 
    def relabel(self, vertexIndex):
        minHeight = None
        for toIndex in range(self.verticesCount):
            if (
                self.graph[vertexIndex][toIndex] - self.preflow[vertexIndex][toIndex]
                > 0
            ):
                if minHeight is None or self.heights[toIndex] < minHeight:
                    minHeight = self.heights[toIndex]
 
        if minHeight is not None:
            self.heights[vertexIndex] = minHeight + 1
 
entrances = [0]
exits = [3]
# graph = [
#     [0, 0, 4, 6, 0, 0],
#     [0, 0, 5, 2, 0, 0],
#     [0, 0, 0, 0, 4, 4],
#     [0, 0, 0, 0, 6, 6],
#     [0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0],
# ]
graph = [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [9, 0, 0, 0]]
 
# prepare our network
flowNetwork = FlowNetwork(graph, entrances, exits)
# set algorithm
flowNetwork.setMaximumFlowAlgorithm(PushRelabelExecutor)
# and calculate
maximumFlow = flowNetwork.findMaximumFlow()
 
print(f"maximum flow is {maximumFlow}")