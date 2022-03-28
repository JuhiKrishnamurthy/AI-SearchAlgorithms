import queue
import sys
import random
from queue import PriorityQueue
import math

class state:
    def __init__(self,w,h, arr,parent =None):
        self.width = w
        self.height = h
        self.blank_pos = (0,0)
        self.arr = []
        self.parent = parent

        for y in range(self.height):
            self.arr.append([])
            for x in range(self.width):
                #print(self.arr[y])
                #print(arr[y][x])
                self.arr[y].append(arr[y][x])
                if (arr[y][x] == 0):
                    self.blank_pos = (x,y)
        
        return

    ## dir can only be one of (0,1),(0,-1),(1,0),(-1,0)            
    def slide(self,dir):
        new_pos_x = self.blank_pos[0]+dir[0]
        new_pos_y = self.blank_pos[1]+dir[1]
        if (new_pos_x <0):
            new_pos_x = 0
        if (new_pos_x >= self.width):
            new_pos_x = self.width -1

        if (new_pos_y <0):
            new_pos_y = 0
        if (new_pos_y >= self.height):
            new_pos_y = self.height -1

        got_new_state = True
        if ( (new_pos_x == self.blank_pos[0]) and 
             (new_pos_y == self.blank_pos[1])):
             got_new_state = False
        
        self.arr[self.blank_pos[1]][self.blank_pos[0]] = self.arr[new_pos_y][new_pos_x]
        self.arr[new_pos_y][new_pos_x] = 0
        self.blank_pos = (new_pos_x,new_pos_y)
        return got_new_state


    def __str__(self):
        retstr =""
        for y in range(self.height):
            for x in range(self.width):
                retstr += f"{self.arr[y][x]},"
            retstr += "\n"

        return retstr

    def __eq__(self,other):
        if ( (self.width != other.width) or 
             (self.height != other.height) or
             (self.blank_pos[0] != other.blank_pos[0]) or 
             (self.blank_pos[1] != other.blank_pos[1]) ):
            return False

        for y in range(self.height):
            for x in range(self.width):
                if (self.arr[y][x] != other.arr[y][x]):
                    return False
        
        return True

def undo_slide_dir(dir):
    undo_dir = dir
    if (undo_dir[0] == 1):
        undo_dir = (-1,0)
    elif (undo_dir[0] == -1 ):
        undo_dir = (1,0)
    elif (undo_dir[1] == 1):
        undo_dir = (0,-1)
    elif (undo_dir[1] == -1):
        undo_dir =(0,1)

    return undo_dir 

"""" Hill Climbing : 
cur state = start
goal state
cost = h(cur_state, goal)
while(not stuck ):
    N = set of next states (cur_state)
    for n in N:
        if (n == goal):
            break (found goal)

        ncost  =h(n,goal)
        if (ncost < cost):
            curstate = n
    if (all costs > prev cost):
        stuck = True
"""

def hill_climb(src_state, goal_state, heuristic_fn):
    path = []
    state_costs =[]
    found_goal = False
    stuck_in_minima = False
    cur_state = state(src_state.width,src_state.height,
                      src_state.arr)

    dir_costs = {(0,1):-1,
                 (0,-1):-1,
                 (1,0):-1,
                 (-1,0):-1}
    

    if (cur_state == goal_state):
        path.append(state(cur_state.width,cur_state.height,
                      cur_state.arr))
        found_goal = True
        return (found_goal,stuck_in_minima,path,state_costs,dir_costs)
        
    
    dir_list = [ (0,1),(0,-1),(1,0),(-1,0)]
    
    stuck_in_minima = False

    #print(f"state: {cur_state}")

    while(1):
        #print(f"{cur_state}")
        path.append(state(cur_state.width,cur_state.height,
                      cur_state.arr))
        
        cost = heuristic_fn(cur_state,goal_state)
        state_costs.append(cost)
        
        if(cur_state == goal_state):
            stuck_in_minima = False
            found_goal = True
            break

        if (stuck_in_minima):
            break

        ## slide in a random dir
        random.shuffle(dir_list)
        
        stuck_in_minima = True

        dir_costs = {(0,1):-1,
                 (0,-1):-1,
                 (1,0):-1,
                 (-1,0):-1}

        for dir in dir_list:
            got_new_state = cur_state.slide(dir)

            #print(f"dir = {dir}")
            #print(f"{cur_state}")
            
            if (not(got_new_state)):
                continue

            scost = heuristic_fn(cur_state,goal_state)
            dir_costs[dir] = scost
            if (scost <cost):
                ## we found a lower cost state;follow this direction, 
                stuck_in_minima = False
                break
            else:
                # undo the sliding and try the next 
                undo_dir = undo_slide_dir(dir)
                cur_state.slide(undo_dir)
    
    return (found_goal,stuck_in_minima,path,state_costs,dir_costs)
        
def num_misplaced(src,tgt):
    n = 0
    for y in range(src.height):
        for x in range(src.width):
            if(src.arr[y][x] != tgt.arr[y][x]):
                n += 1
    return n

def minkowski_dist(src_array,w,h, tgt_value_pos_dict, p):
    ## for each value in src_array, find where it is in the target
    ## compute the distance and sum

    ##the blank tile value is 0, 
  
    dist = 0
    for y in range(0,h):
        for x in range(0,w):
            val = src_array[y][x]
            tgt_pos = tgt_value_pos_dict[val]
            dist += math.pow(abs(y - tgt_pos[1]),p)
            dist += math.pow(abs(x - tgt_pos[0]),p)
    
    dist = math.pow(dist,1.0/float(p))
    return dist

def trace_path(tstate):
    path = [tstate]
    cur_state =tstate
    while(not (cur_state.parent is None)):
        path.insert(0,cur_state.parent)
        cur_state = cur_state.parent
    return path
    
def find_state_in_list(lst,s):
    for l in lst:
        if (l == s):
            return True
    return False

def best_first(src_state, goal_state, heuristic_fn):

    ## states will be stored here
    #  to  check if node is in open queue
    OPEN_NODES = []

    # tuples (hval, state)
    OPEN = queue.PriorityQueue()

   ## states will be stored here
    # to  check if node is in closed set
    CLOSED = []

    cur_state = state(src_state.width,src_state.height,
                      src_state.arr,parent=None)
    cost = heuristic_fn(cur_state,goal_state)

    found_goal =False
    final_state = None
    dir_list = [ (0,1),(0,-1),(1,0),(-1,0)]
    OPEN.put((cost,id(cur_state),cur_state))
    OPEN_NODES.append(cur_state)

    while( OPEN.empty()== False):
        (c,i,s) = OPEN.get()

        for x in OPEN_NODES:
            if (x == s):
                OPEN_NODES.remove(x)

        if (s==goal_state):
            found_goal =True
            final_state = s
            break
        
        #add s to closed
        CLOSED.append(s)

        # expand s
        child_states = queue.PriorityQueue()
       
        for dir in dir_list:
            ns = state(s.width,s.height,s.arr,parent=s)
            ns.slide(dir)
            ns_cost = heuristic_fn(ns,goal_state)
            child_states.put((ns_cost,id(ns),ns))

            if (ns == goal_state):
                found_goal =True
                final_state = ns
                break

        if(found_goal):
            break

        while(child_states.empty() == False):
            (c,i,ss) = child_states.get()
            if (not(find_state_in_list(CLOSED,ss)) and
                not(find_state_in_list(OPEN_NODES,ss))):
                OPEN.put( (c,id(ss),ss))
                OPEN_NODES.append(ss)
                break

    #print(f"final state: {final_state}")
    path_to_final = []
    if (not(final_state is None)):
        print("FOUND goal state")
        path_to_final = trace_path(final_state)

    for p in path_to_final:
        print(p)
    return

def hill_climb_main():

    height = 3
    width = 3

    start = [[2,0,3],[1,8,4],[7,6,5]]
    goal = [[1,2,3],[8,0,4],[7,6,5]]

    start_state = state(width,height,start)
    goal_state = state(width,height,goal)

    found_goal,stuck_in_minima,path,state_costs,dir_costs = hill_climb(start_state,goal_state,num_misplaced)

    if (found_goal):
        print("FOUND GOAL!")
    else:
        print("Got Stuck :(")
    print(f"Path length: {len(path)}")
    for p in path:
        print(p)
    print(state_costs)
    print(dir_costs)

def best_first_main():
    height = 3
    width = 3

    start = [[2,0,3],[1,8,4],[7,6,5]]
    goal = [[1,2,3],[8,0,4],[7,6,5]]

    goal_dict = {}
    for y in range(height):
        for x in range(width):
            goal_dict[goal[y][x]] = (x,y)

    start_state = state(3,3,start)
    goal_state = state(3,3,goal)
    best_first(start_state, goal_state,
                man_dist 
               #num_misplaced
               )

    return

if __name__ == "__main__":
    best_first_main()
    





        

        







