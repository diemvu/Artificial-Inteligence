Name : Diem Vu



First State: "123456789AB DEFC"
BFS: 1, 3, 1, 3
DFS: 1, 3, 1, 3
DLS 2 : 1, 3, 1, 3
GBFS h1: 1, 3, 1, 3
GBFS h2: 1, 3, 1, 3
AStar h1: 1, 3, 1, 3
AStar h2: 1, 3, 1, 3

Second State: "123456789ABC DFE"
BFS: 7, 16, 7, 10
DFS: 7, 10, 3, 8
DLS 2: -1, 0, 0, 0
GBFS h1: 7, 40, 13, 28
GBFS h2: 7, 16, 5, 12
AStar h1: 7, 88, 31, 58
AStar h2: 7, 87, 30, 58


Time complexity:

BFS: 
4 is maximum successors
d is depth of shallowest solution 
O(4^d)

DFS:
4 is maximum successors
m is maximum depth 

DLS with maxDepth l:
4 is maximum successors
O(4^l)

GBFS:
4 is maximum successors
d is maximum depth 
O(4^d)

AStar:
4 is maximum successors
d is maximum depth 
O(4^m)

