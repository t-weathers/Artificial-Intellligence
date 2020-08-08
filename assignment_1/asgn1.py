import sys
from collections import deque
from collections import defaultdict 

def main():

    if(len(sys.argv) != 5):
        print("ERROR: incorrect arguments")
        return 1

    start_state = [
        [-1,-1,-1],
        [-1,-1,-1]
    ]
    goal_state = [
        [-1,-1,-1],
        [-1,-1,-1]
    ]
    current_state = [
        [0,0,0],
        [0,0,0]
    ]

    start_state = readFile(sys.argv[1]) #read arg1 into start state
    goal_state = readFile(sys.argv[2])  #read arg2 into end state
    print("START: ", start_state)
    print("GOAL: ",goal_state)

    
    MODE = sys.argv[3]  #mode
    if(not verify_mode(MODE)):
        print ("invalid MODE")
        return 1
    
    print("MODE: " + MODE)

    outFile = open(sys.argv[4],'w') #open outfile for writing

    
    current_state = start_state
    #print("CURRENT: ",str(current_state))
    outFile.write("MODE: " + str(MODE) + "\n\n")
    outFile.write("START STATE: \n")
    outFile.write(str(current_state[0]).strip('[]')+'\n')
    outFile.write(str(current_state[1]).strip('[]')+'\n')
    outFile.write('\n')

    outFile.write("GOAL STATE: \n")
    outFile.write(str(goal_state[0]).strip('[]')+'\n')
    outFile.write(str(goal_state[1]).strip('[]')+'\n')
    outFile.write('\n')

    #outFile.write("Start: "+str(current_state.strip('[]')))
    if(MODE == "bfs"):

        path = bfs2(current_state,goal_state)
        if(path != 0):
            outFile.write("!!VIABLE PATH FOUND!!\n")
            writeMatrix3_to_file(path,outFile)
            outFile.write("Nodes Expanded: " + str(path[1]))
            print("Nodes Expanded: ",path[1])
        else:
            outFile.write("--------------\n")
            outFile.write("no found path\n")
            outFile.write("--------------\n")
        
    elif(MODE == "dfs"):
        path = dfs(current_state,goal_state)
        if(path != 0):
            outFile.write("VIABLE PATH FOUND\n")
            writeMatrix3_to_file(path,outFile)          #write to file and print path
            outFile.write("Nodes Expanded: " + str(path[1]))
            print("Nodes Expanded: ",path[1])
        else:
            outFile.write("--------------\n")
            outFile.write("no found path\n")
            outFile.write("--------------\n")

    elif(MODE == "iddfs"):
        ########################
        ########################
        max_depth = sys.maxsize
        ########################
        ########################
        path = iddfs(current_state,goal_state,max_depth)
        outFile.write("MAX DEPTH: "+ str(max_depth) + "\n\n")
        if path != 1:
            outFile.write("VIABLE PATH FOUND\n")
            writeMatrix3_to_file(path,outFile)          #write to file and print path
            outFile.write("Nodes Expanded: " + str(path[1]))
            print("Nodes Expanded: ",path[1])
        else:
            outFile.write("--------------\n")
            outFile.write("no found path\n")
            outFile.write("--------------\n")

    elif(MODE == "astar"):
        path = astar(current_state,goal_state)
        if(path != 0):
            outFile.write("VIABLE PATH FOUND\n")
            writeMatrix3_to_file(path,outFile)          #write to file and print path
            outFile.write("Nodes Expanded: " + str(path[1]))
            print("Nodes Expanded: ",path[1])
        else:
            outFile.write("--------------\n")
            outFile.write("no found path\n")
            outFile.write("--------------\n")
        
    else:
        print("error on modes")
        return 1
    
    #print(valid1_0(current_state))
    #print(valid2_0(current_state))
    #print(valid0_1(current_state))
    #print(valid1_1(current_state))
    #print(valid0_2(current_state))


    outFile.close()
    return 0


def verify_mode(mode):  #verify that the mode is allowed for the program
    if(mode != "bfs" and mode != "dfs" and mode != "iddfs" and mode != "astar"):
        return False
    else:
        return True

def readFile(argument): #read in file for start state and goal state
    inFile = open(argument, 'r') #open the infile of start location
    if(inFile == None):
        print("error opening file")
        return 1
    array = [
        [-1,-1,-1],
        [-1,-1,-1]
    ]
    for b in range(0,2):
        line = inFile.readline()
        counter = 0
        array[b] = line.split(',')  #separated by a comma
        
    array[0] = [int(i) for i in array[0]]
    array[1] = [int(i) for i in array[1]]

    inFile.close()
    return array

#check if piece is THERE to move, moving will cause end on sent side, moving will cause end on recieve side
def valid1_0(current_state):
    if current_state[0][2] == 1:   #boat on top side
        if(current_state[0][0] >= 1 and (current_state[0][0] - 1 >= current_state[0][1]) and current_state[1][0] + 1 >= current_state[1][1]):
            return True
    else:   #boat on bottom side
        if(current_state[1][0] >= 1 and (current_state[1][0] - 1 >= current_state[1][1]) and current_state[0][0] + 1 >= current_state[0][1]):
            return True
    return False
    
def valid2_0(current_state):
    if current_state[0][2] == 1:   #boat on top side
        if(current_state[0][0] >= 2 and (current_state[0][0] - 2 >= current_state[0][1]) and current_state[1][0] + 2 >= current_state[1][1]):
            return True
    else:   #boat on bottom side
        if(current_state[1][0] >= 2 and (current_state[1][0] - 2 >= current_state[1][1]) and current_state[0][0] + 2 >= current_state[0][1]):
            return True
    return False

def valid0_1(current_state):
    if current_state[0][2] == 1:   #boat on top side
        if(current_state[0][1] >= 1  and (current_state[1][1] + 1 <= current_state[1][0] or current_state[1][0] == 0)):
            return True
    else:   #boat on bottom side
        if(current_state[1][1] > 0 and (current_state[0][1] + 1 <= current_state[0][0] or current_state[0][0] == 0)):
            return True
    return False

def valid1_1(current_state):
    if current_state[0][2] == 1:   #boat on top side
        if(current_state[0][1] > 0 and current_state[0][0] > 0 ):
            return True
    else:   #boat on bottom side
        if(current_state[1][1] > 0 and current_state[1][0] > 0):
            return True
    return False

def valid0_2(current_state):
    if current_state[0][2] == 1:   #boat on top side
        if(current_state[0][1] > 1 and (current_state[1][1] + 2 <= current_state[1][0] or current_state[1][0] == 0)):
            return True
    else:   #boat on bottom side
        if(current_state[1][1] > 1 and (current_state[0][1] + 2 <= current_state[0][0] or current_state[0][0] == 0)):
            return True
    return False

def findPossibleMoves(current_state):
    possible = []
    if current_state[0][2] == 1:    #boat on top
        if valid1_0(current_state): #move one chickens
            possible.append([
                [current_state[0][0]-1,current_state[0][1],current_state[0][2]-1],
                [current_state[1][0]+1,current_state[1][1],current_state[1][2]+1]
            ])

        if valid2_0(current_state):   #move two chickens
            possible.append([
                [current_state[0][0]-2,current_state[0][1],current_state[0][2]-1],
                [current_state[1][0]+2,current_state[1][1],current_state[1][2]+1]
            ])

        if valid0_1(current_state):   #move one wolf
            possible.append([
                [current_state[0][0],current_state[0][1]-1,current_state[0][2]-1],
                [current_state[1][0],current_state[1][1]+1,current_state[1][2]+1]
            ])

        if valid1_1(current_state):   #move one each
            possible.append([
                [current_state[0][0]-1,current_state[0][1]-1,current_state[0][2]-1],
                [current_state[1][0]+1,current_state[1][1]+1,current_state[1][2]+1]
            ])
        if valid0_2(current_state):
            possible.append([
                [current_state[0][0],current_state[0][1]-2,current_state[0][2]-1],
                [current_state[1][0],current_state[1][1]+2,current_state[1][2]+1]
            ])
    else:   #boat on bottom
        if valid1_0(current_state): #move one chickens
            possible.append([
                [current_state[0][0]+1,current_state[0][1],current_state[0][2]+1],
                [current_state[1][0]-1,current_state[1][1],current_state[1][2]-1]
            ])

        if valid2_0(current_state):   #move two chickens
            possible.append([
                [current_state[0][0]+2,current_state[0][1],current_state[0][2]+1],
                [current_state[1][0]-2,current_state[1][1],current_state[1][2]-1]
            ])

        if valid0_1(current_state):   #move one wolf
            possible.append([
                [current_state[0][0],current_state[0][1]+1,current_state[0][2]+1],
                [current_state[1][0],current_state[1][1]-1,current_state[1][2]-1]
            ])

        if valid1_1(current_state):   #move one each
            possible.append([
                [current_state[0][0]+1,current_state[0][1]+1,current_state[0][2]+1],
                [current_state[1][0]-1,current_state[1][1]-1,current_state[1][2]-1]
            ])
        if valid0_2(current_state):
            possible.append([
                [current_state[0][0],current_state[0][1]+2,current_state[0][2]+1],
                [current_state[1][0],current_state[1][1]-2,current_state[1][2]-1]
            ])
    return possible


def bfs(current_state,goal_state):
    explored = {}
    unexplored = []
    unexplored.append([current_state])
    nodes_expanded = 0
    while True:
        if len(unexplored) == 0:
            print ("BFS Failure, couldnt solve the problem!")
            return 0
        current_path = unexplored.pop(0)
        current = current_path[-1]
        nodes_expanded += 1
        if current == goal_state:
            print("FOUND GOAL STATE!")
            return (current_path,nodes_expanded)
        #explored.append(current)
        explored[str(current)] = current_path
        next_moves = findPossibleMoves(current)
        for i in next_moves:
            if str(i) not in explored:
                path = list(current_path)
                path.append(i)
                unexplored.append(path)

def bfs2(current_state,goal_state):
    explored = {}
    unexplored = deque()
    unexplored.append([current_state])
    nodes_expanded = 0
    while True:
        if len(unexplored) == 0:
            print ("BFS Failure, couldnt solve the problem!")
            return 0
        #print(unexplored)
        #print()
        current_path = unexplored.popleft()
        current = current_path[-1]
        nodes_expanded += 1
        #print("CURRENT: ",current)
        if current == goal_state:
            print("FOUND GOAL STATE!")
            return (current_path,nodes_expanded)
        explored[str(current)] = current_path
        #expand options into explored
        next_moves = findPossibleMoves(current)
        #print("exp",explored)
        for i in next_moves:
            if str(i) not in explored and (i not in unexplored):
                path = list(current_path)
                path.append(i)
                unexplored.append(path)




def dfs(current_state,goal_state):
    explored = {}
    unexplored = []
    unexplored.append([current_state])
    nodes_expanded = 0
    while True:
        if len(unexplored) == 0:
            print ("DFS Failure, couldnt solve the problem!")
            return 0
        current_path = unexplored.pop()
        current = current_path[-1]
        nodes_expanded += 1
        #print("CURRENT: ",current)
        if current == goal_state:
            print("FOUND GOAL STATE!")
            return (current_path,nodes_expanded)
        explored[str(current)] = current_path
        #expand options into explored
        next_moves = findPossibleMoves(current)
        #print("Available moves: ",next_moves)
        for i in next_moves:
            if str(i) not in explored:
                path = list(current_path)
                path.append(i)
                unexplored.append(path)

def modified_dfs(current_state,goal_state,max_depth):
    explored = {}
    unexplored = []
    unexplored.append([current_state])
    nodes_expanded = 0
    #depth = 0
    while True:
        if len(unexplored) == 0:
            return nodes_expanded

        current_path = unexplored.pop(-1)
        current = current_path[-1]
        nodes_expanded += 1
        #print("CURRENT: ",current)
        if current == goal_state:
            print("FOUND GOAL STATE!")
            
            return (current_path,nodes_expanded)
        explored[str(current)] = current_path
        #expand options into explored
        next_moves = findPossibleMoves(current)
        #print("Available moves: ",next_moves)
        for i in next_moves:
            if str(i) not in explored:
                if (len(current_path) < max_depth):
                    path = list(current_path)
                    path.append(i)
                    unexplored.append(path)
        


def iddfs(current_state,goal_state,maxDepth):
    nodes_visited = 0
    for i in range(0,maxDepth):
        print("starting depth of search: ",i)
        path = modified_dfs(current_state,goal_state,i)
        if (type(path) == int):
            nodes_visited += path
            #print(nodes_visited)
            continue
        else:
            return (path[0], nodes_visited + path[1])
    print("Unable to find Goal State in maxDepth: ",maxDepth)
    return 1


def astar(current_state,goal_state):
    explored = {}
    unexplored = []
    #unexplored.append([(current_state,0)])
    

    nodes_expanded = 0
    while True:
        if len(unexplored) == 0:
            print ("Astar Failure, couldnt solve the problem!")
            return 0
        #print("unexplored: ",unexplored)
        #current_path = unexplored.pop(-1)[0]
        #print("current_path: ",current_path)
        current_path = unexplored.pop(-1)
        current = current_path[-1]

        #current = current_path[0]
        #print("current: ",current)
        nodes_expanded += 1
        if current == goal_state:
            print("FOUND GOAL STATE!")
            return (current_path,nodes_expanded)
        explored[str(current)] = current_path
        next_moves = findPossibleMoves(current)
        #print("NM: ",next_moves)
        for i in next_moves:
            if str(i) not in explored:

                path = list(current_path)
                path.append(i)
                unexplored.append(path)

                #print(unexplored)
                #unexplored = insert_pq(unexplored,i,current_path,goal_state)
                #print(unexplored)
                #instead of appending, make this a priority queue
                #need a hueristic function to determine the best path of the new options and make a working pqueue
                
def insert_pq(array,node,path,goal_state):
    score = hueristic(node,goal_state)
    newpath = list(path)
    newpath.append(node)
    if(len(array) == 0):
        array.append((newpath,score))
    else:
        for i in array:
            if score <= array[i][1]:
                array.insert(i,(newpath,score))

    return array


def writeMatrix3_to_file(matrix, fileOut):
    print("PATH: ")
    fileOut.write('\n')
    fileOut.write("PATH: \n")
    for x in matrix[0]:
        for z in x:
            out_line = str(z).strip('[]')
            print(out_line)
            fileOut.write(out_line)
            fileOut.write('\n')
        fileOut.write('\n')
        print()

def hueristic(current_state,goal_state):
    if current_state == goal_state:
        return 0
    sum = 0
    sum += abs(goal_state[0][0] - current_state[0][0])
    sum += abs(goal_state[0][1] - current_state[0][1])
    sum += abs(goal_state[1][0] - current_state[1][0])
    sum += abs(goal_state[1][1] - current_state[1][1])
    sum += abs(goal_state[0][2] - current_state[0][2])
    sum += abs(goal_state[1][2] - current_state[1][2])
    return sum

main()
