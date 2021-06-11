# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 10:09:00 2021

@author: rpthi

Problem:
Given a list of cities and distances between each pair of cities, determine the
optimal aka shortest route to visit all cities once and return to original city.

ie
given a complete (Kn) graph with weighted edges (as an adj MATRIX), what is the
Hamiltonian cycle (path visiting each node once) of minimum cost?

Finding optimal solution is very hard; problem is called NP-Complete
Brute force: O(n!)
Dynamic Programming Algorithms: O(n^2 * 2^n)
Although, there do exist some approximation algorithms that run quickly

idea:
compute optimal solution for paths of length N while reusing information
    from previously known partial tours of length N-1
    AKA Every subpath of a path of minimum distance is itself of minimum distance. 
Before starting, make sure to select a node 0 <= S < N to be designated start node
Then, compute and store the optimal value from S to each node X (/=S). This will solve
TSP for all paths of length n = 2 (directly from adjacency matrix)
To compute for paths of length n = 3, we need to store two things from each S-X from n=2,
    a) set of all visited nodes in the subpath
    b) the index of last visited node in the path
Togther, these form a dynamic programming state. There are N possible nodes we could have
visited last and 2^N possible subsets of visited nodes. Hence, the space needed to store
the answer to each subproblem is bounded by O(N * 2^N)

a problem: Storing takes time and space, we don't want to have to loop to analyze visited
            and a queue doesn't make much sense here
the solution: representing set of visited nodes as a 32-bit integer, allows
                easy caching in a memo table AKA bit field of 0000, 0001 etc

Now, to solve 3 <= n <= N, we're going to take the solved subpaths from n-1 and add another
edge extending to a node not visited from last visited node (which has been saved)
do this for all neighbors (remember, KN [complete graph]). Do this until all paths are 
of length n

to complete tour, connect back to S. Loop over the end state [ie where the binary 
representation is composed of N 1's] in the memo table for every possible end position
and minimize lookup value plus cost of going back to S

"""
import numpy as np
# finds the minimum TSP tour cost
# adj - adjacency matrix
# node - start node 0<=S<N

def tsp(adj, node):
    N, _ = np.shape(adj) # should be (N,N) so not an issue
    # initialize 2d memo table
    # fill table with infinity or None
    # memo table of size N by 2^N, note memo table is empty to begin

    memo = np.zeros([N,2**N], np.int32)
    
    setup(adj, memo, node, N)
    #print(memo)
    solve(adj, memo, node, N)
    minCost = find_min_cost(adj, memo, node, N)
    tour = find_best_tour(adj, memo, node, N)
    return minCost, tour
    
# initializes memo table by caching optimal solution from the start node
# to every other node
def setup(adj, memo, node, N):
    for i in range(N):
        if i == node: continue
        # Store optimal value from node (start) to each node i
        # given as input from adj matrix
        memo[i][1 << node | 1 << i] = adj[node][i]
        
    
def solve(adj, memo, node, N):
    for i in range(3, N+1):
        # combinations function generates all bit sets of size N with i bits set to 1
        # ex: combinations(3,4) = {0111, 1011, 1101, 1110}
        for subset in combinations(i, N):
            if not_in(node, subset): continue
            for next_node in range(N):
                if next_node == node or not_in(next_node, subset): continue
                # subset state without next_node
                state = subset ^ (1 << next_node)
                minDist = float('Infinity')
                for end_node in range(N):
                    if end_node == node or end_node == next_node or not_in(end_node, subset):
                        continue
                    newDistance = memo[end_node][state] + adj[end_node][next_node]
                    if newDistance < minDist: minDist = newDistance
                memo[next_node][subset] = minDist


def find_min_cost(adj, memo, node, N):
    # the end state is the bit mask with N bits set to 1 aka 2^N - 1
    END_STATE = (1 << N) -1
    minCost= float('Infinity')
    for end_node in range(N):
        if end_node == node: continue
        cost = memo[end_node][END_STATE] + adj[end_node][node]
        if cost < minCost:
            minCost = cost
    return minCost

def find_best_tour(adj, memo, node, N):
    lastIndex = node
    state = (1 << N) - 1 # end state
    tour = [None] * (N+1)
    #start at end, and go backwards
    for i in range(N-1, 0, -1):
        index = -1
        for j in range(N):
            if j == node or not_in(j, state): continue
            if index == -1: index = j
            prevDist = memo[index][state] + adj[index][lastIndex]
            newDist = memo[j][state] + adj[j][lastIndex]
            if newDist < prevDist: index = j
        
        tour[i] = index
        state = state ^ (1 << index)
        lastIndex = index
        
    tour[0] = tour[N] = node
    return tour
                    
# returns true if the ith bit in 'subset' is not set            
def not_in(i, subset):
    return ((1 << i) & subset) == 0 #None?

def combinations(i, N):
    subsets = []
    generate_bit_sets(0,0,i,N,subsets)
    return subsets

# recursive function to generate bit sets
def generate_bit_sets(set_, at, i, N, subsets):
    if i == 0:
        subsets.append(set_)
    else:
        for j in range(at, N):
            #flip on jth bit
            set_ = set_ | (1 << j)
            generate_bit_sets(set_, j+1, i-1, N, subsets)
            #backtrack and flip off jth bit
            set_ = set_ & ~(1 << j)
            
#adj must be np array
#might have to go back and adjust the ranges N is stop value, so it stops once it reaches that
#might have to change it to N+1 or N-1

adj = np.array([[0, 4, 1, 9], [3, 0, 6, 11],
            [4, 1, 0, 2], [6, 5, -4, 0]])

minCost, tour = tsp(adj, 0)
print(minCost)
print(tour)