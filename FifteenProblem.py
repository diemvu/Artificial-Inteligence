#diem vu
#assignment 1
#TCSS 435


import sys
from copy import deepcopy

solution1 =['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',' ']
solution2 = ['1','2','3','4','5','6','7','8','9','A','B','C','D','F','E',' ']
actions = 'RDLU'

#a class hold the output
class Result:
    depth = -1
    numCreated = 0
    numExpanded = 0
    maxFringe = 0
    #string representation of result
    def __str__(self):
        result = str(self.depth) +', ' + str(self.numCreated)+', '+ str(self.numExpanded)+', '+ str(self.maxFringe)
        return result

# a puzzle
class PuzzleState:
    state =None  #list of all the tiles in order
    blankIndex =None # index of the blank tile

    def __init__(self,initialState):
        self.state = list(initialState)
        self.depth = 0
        self.blankIndex = self.state.index(" ")

    def __eq__(self,x):
        return self.state == x.state

    # return succesors of a tile 
    def getSuccesors(self):
        successors =[]
        successor = None
        for action in actions :
            #move the blank tile to the right
            if action =='R' and self.blankIndex % 4 <3 :
                successor = deepcopy(self)
                nextposition = self.blankIndex +1

            #move the blank tile down
            elif action =='D' and self.blankIndex <12 :
                successor = deepcopy(self)
                nextposition = self.blankIndex +4

            #move the blank tile left
            elif action == 'L' and self.blankIndex %4 > 0:
                successor = deepcopy(self)
                nextposition = self.blankIndex -1

            #move the tile up
            elif action == 'U' and self.blankIndex >3:
                successor = deepcopy(self)
                nextposition = self.blankIndex -4
            # add successor to the successors list
            if successor:
                # succesor depth = preceding state 's depth
                successor.depth +=1
                #move blank tile to its target 
                successor.state[successor.blankIndex] = successor.state[nextposition]
                successor.state[nextposition] =' '
                successor.blankIndex = nextposition
                successors.append(successor)
        return successors

    # h1 is equal to the number of non-blank misplaced tiles 
    def h1(self):
        count = 0
        state = self.state
        for i in range(16):
            if state[i] != solution1[i] and state[i] != ' ':
                count +=1
        return count

    #h2 is equal to sum of horizontal and vertical distance of each misplaced tile to its place in solution
    def h2(self):
        state = self.state
        ManhattanDistance = 0
        for i in range(16):
            if state[i] != ' ':
                solutionIndex = solution1.index(state[i])
                xDistance = abs(solutionIndex %4 - i%4)
                yDistance = abs(int(solutionIndex /4) - int(i/4))
                ManhattanDistance = ManhattanDistance+ xDistance + yDistance
        return ManhattanDistance

#priority queue for AStar and GBFS 
class PriotityQueue():
    Heuristics =[]
    Nodes = []
    size = 0
    
    #put a node into a priority queue
    def put(self, node, heurisitic):
        self.size +=1
        for i in range(len(self.Nodes)):
            if heurisitic < self.Heuristics[i]:
                self.Heuristics.insert(i, heurisitic)
                self.Nodes.insert(i, node)
                return
        self.Heuristics.append(heurisitic)
        self.Nodes.append(node)

    #pop a node out of priority queue    
    def pop(self):
        if self.Nodes:
            self.size -=1
            self.Heuristics.pop(0)
            return self.Nodes.pop(0)

# all the search algorithms are in this class   
class SearchAlgorithm:

    def BFS(self,initialPuzzleState):
        result = Result()
        queue = []  # queue FIFO
        explored = []
        #put the initial state into the queue
        queue.append(initialPuzzleState)
        #print(str(queue))
        count =0
        while queue:
            if len(queue) > result.maxFringe:
                result.maxFringe = len(queue)
            node = queue.pop(0)
            # put the expanded node into explored list
            explored.append(node)

            #return if solution is found
            if node.state == solution1 or node.state == solution2:
                result.depth = node.depth
                return result
            result.numExpanded+=1
            successors = node.getSuccesors()

            # if succesor has not been expanded, put it into the queue
            for succesor in successors:  
                if (succesor not in explored) and (succesor not in queue):
                    result.numCreated +=1
                    queue.append(succesor)
        return Result()

    def DFS(self,initialPuzzleState):
        result = Result()
        stack =[]   #stack FILO
        explored = []
        #put the initial state into the stack
        stack.append(initialPuzzleState)
        while stack:
            if len(stack) > result.maxFringe:
                result.maxFringe = len(stack)
            node = stack.pop()

            #return if solution is found
            if (node.state == solution1) or (node.state == solution2):
                result.depth = node.depth
                return result
            else:
                result.numExpanded +=1
                successors = node.getSuccesors()
                successors.reverse()
                # if succesor has not been expanded, put it into the queue
                for successor in successors:
                    if (successor not in explored) :
                        stack.append(successor)
                        result.numCreated +=1
                explored.append(node)
        return Result()

    #similar to DFS but only expand to maxDepth depth. the node at maxDepth is considered having no successors
    def DLS(self,initialPuzzleState,maxDepth):
        result = Result()
        stack =[]   #stack FILO
        explored = []
        stack.append(initialPuzzleState)
        
        while stack:
            if len(stack) > result.maxFringe:
                result.maxFringe = len(stack)
            node = stack.pop()
            if (node.state == solution1) or (node.state == solution2):
                result.depth = node.depth
                return result
            else:
                if node.depth >maxDepth:
                    break
                result.numExpanded +=1
                successors = node.getSuccesors()
                successors.reverse()
                for successor in successors:
                    if (successor not in explored) :
                        stack.append(successor)
                        result.numCreated +=1
                explored.append(node)
        return Result()

    #similar to BFS but the ordered of successor to be expanded is based on its heuristic
    def GBFS(self,initialPuzzleState,heuristic):
        result = Result()
        queue = PriotityQueue()   #
        explored = []
        cost = 0
        #calculate a node heuristic
        if heuristic == 'h1':
            cost = initialPuzzleState.h1()
        if heuristic == 'h2':
            cost = initialPuzzleState.h2()

        queue.put(initialPuzzleState,cost)
        while queue.size>0:
            if queue.size > result.maxFringe:
                result.maxFringe = queue.size
            node = queue.pop()
            if node.state == solution1 or node.state == solution2:
                result.depth = node.depth
                return result
            else:
                result.numExpanded +=1
                successors = node.getSuccesors()
                for successor in successors:
                    if successor not in explored:
                        if heuristic =='h1':
                            h = successor.h1()
                        if heuristic =='h2':
                            h = successor.h2()
                        queue.put(successor,h)
                        result.numCreated +=1
                explored.append(node)
        return Result()
    # similar to GBFS but its cost is the sum of a node's depth and its heuristic
    def AStar(self,initialPuzzleState,heuristic):
        result = Result()
        queue = PriotityQueue()   
        explored = []
        cost = 0
        if heuristic == 'h1':
            cost = initialPuzzleState.depth + initialPuzzleState.h1()
        if heuristic == 'h2':
            cost = initialPuzzleState.depth + initialPuzzleState.h2()
 
        
        queue.put(initialPuzzleState,cost)
        while queue.size>0:
            if queue.size > result.maxFringe:
                result.maxFringe = queue.size
            node = queue.pop()
            if node.state == solution1 or node.state == solution2:
                result.depth = node.depth
                return result
            result.numExpanded +=1
            successors = node.getSuccesors()
            for successor in successors:
                if successor not in explored:
                    if heuristic =='h1':
                        h = successor.h1()
                    if heuristic =='h2':
                        h = successor.h2()
                    cost = h + successor.depth
                    queue.put(successor,cost)
                    result.numCreated +=1
            explored.append(node)
        return Result()


    def main(self):
        solver = SearchAlgorithm()
        result = None
        start = None
        searchingMethod = None
        maxDepth = None
        heuristic = None

        instruction = sys.argv
        #first argument is the file's name
        string = instruction[1] # the puzzle state
        if len(instruction) in range(3,5):
            start = PuzzleState(string)
            searchingMethod = instruction[2]
            if len(instruction) == 4:
                heuristic = instruction[3]
        else:
            print(" Invalid instruction ")
            sys.exit(-1)
        
        if sorted(string) != sorted(solution1):
            print("Invalid puzzle")
        
        if searchingMethod =='BFS':
            result = solver.BFS(start)
        elif searchingMethod =='DFS':
            result = solver.DFS(start)
        elif searchingMethod == 'DLS':
            result = solver.DLS(start,int(heuristic))
        elif searchingMethod =='GBFS':
            result = solver.GBFS(start,heuristic)
        elif searchingMethod == 'AStar':
            result = solver.AStar(start,heuristic) 
        print(result)

if __name__ =='__main__':
    problem = SearchAlgorithm()
    problem.main()

            
            

            

   


