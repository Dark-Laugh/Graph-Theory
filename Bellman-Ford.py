'''
Created on Fri May 309 11:38:29 2021

@author: rpthi

Bellman-Ford is a SSSP (Single Source Shortest Path) algorithm.
However, it is not ideal since it has a time complixity of O(EV). It is better
to use Dijkstra's.
HOWEVER, Dijkstra's fails with negative edge weights. Hence, we can use BF
if a graph has negative edge weights since BF finds negative cycles.

A neat application of BF is performing an arbitrage:
In economics and finance, arbitrage is the practice of taking advantage of a
price difference between two or more markets: striking a combination of
matching deals that capitalize upon the imbalance, the profit being the
difference between the market prices at which the unit is traded

Explanation:
Start at source node
Goes through each edge performing relaxation operations (meauring distance then
                                                         not touching edge again)
    does this V-1 number of times total to ensure propogation (V vertices means source node 
                                                       can have V-1 edges)
    
Then it examines for negative cycles by repeating the each edge performing 
    relaxation operations. However, this time, if the distance in dist array
    collected before is less than the new distance found, negative cycle and so
    avoid
Further, nodes reachable by negative cycle are marked down as well, since they
would not be reached otherwise (obviously as those in the negative cycle)
Repeat V-2 times to ensure propogation
'''

#iterates over each edge, so here it is simpler to use an edge list
#since I will be using an edge list, it is simpler to have a graph class where
#number of vertices is known

class Graph:
    def __init__(self, num_v):
        self.num_v = num_v
        self.edges = [] #arr edges
    
    def add_edge(self, v1, v2, weight):
        self.edges.append([v1,v2,weight])
    
    def BF(self, node):
        dist = [float('Infinity')] * self.num_v
        dist[node] = 0 #dist node to itself is clearly 0
        prev = [None] * self.num_v      
        #relaxation operations num_v - 1 times
        for _ in range(self.num_v -1):
            #iterate over each edge
            for v1,v2,weight in self.edges:
                if dist[v1] != float('infinity') and dist[v1] + weight < dist[v2]:
                    #if the distance of a node to another node is defined, and dsistance + weight
                    #is less than distance of second node to first node, then distance of second
                    #node to first node is first node + weight.
                    dist[v2] = dist[v1] + weight
                    prev[v2] = v1
                    
        # iterate over each edge again,
        # if value changes then we have a negative cycle in the graph
        # and we cannot find the shortest distances
        for v1,v2,weight in self.edges:
            if dist[v1] != float('infinity') and dist[v1] + weight < dist[v2]: 
                print('Negative cycle, cannot compute distances')
                return
        #no negative cycle
        #self.print_solution(dist)  
        return dist, prev
    
    def print_solution(self, dist):
        print("Distance of vertexes from source:")
        for i in range(self.num_v):
            print("{0}\t\t{1}".format(i, dist[i]))
   
    def find_shortest_path(self, start_node, end_node):
        dist, prev = self.BF(start_node)
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
         
g = Graph(5)
g.add_edge(0, 1, 1)
g.add_edge(0, 2, 7)
g.add_edge(1, 3, 3)
g.add_edge(2, 1, 6)
g.add_edge(3, 2, 2)

print(g.find_shortest_path(0, 2))