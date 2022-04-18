#name: juhi krishnamurthy
#roll number: 102003043
import queue
import sys
import random
import math

class State:
    def __init__(self,
                blocks_dict =None, 
                top_blocks_set = None,
                allowed_moves_set =None,
                parent =None):

        self.blocks_dict = {}
        if (not(blocks_dict is None)):
            for k in blocks_dict:
                self.blocks_dict[k] = blocks_dict[k]

        self.parent = parent

        if (top_blocks_set is None):
            self.top_blocks_set = set([])
            self.set_all_top_blocks()
            self.allowed_moves_set =set([])
            self.set_allowed_moves()
        else:
            self.top_blocks_set = set(list(top_blocks_set))
            self.allowed_moves_set =set(list(allowed_moves_set))
            
        return

    def __str__(self):
        ret_str = ""
        def add_to_str(blk):
            if not (blk is None):
                u,d = self.blocks_dict[blk]
                ret_str =add_to_str(d)
                return ret_str + f"{blk},"
            else:
                return ""

       
        for b in self.top_blocks_set:
            n = b
            while not(n is None):
                ret_str = ret_str +f"{n},"
                n = self.blocks_dict[n][1]
            ret_str = ret_str + "\n"
        #ret_str = str(self.blocks_dict)#str(self.top_blocks_set)
        return ret_str

    def is_top_blk(self,blk):
        if (not(blk in self.blocks_dict)):
            return False
        u,d = self.blocks_dict[blk]
        if (u is None):
            return True
        else:
            return False

    def set_all_top_blocks(self):
        self.top_blocks_set = set([])
        for k in self.blocks_dict:
            if (self.is_top_blk(k)):
                self.top_blocks_set.add(k)
        return

    def set_allowed_moves(self):
        for blk in self.top_blocks_set:
            if not(self.blocks_dict[blk][1] == None):
                self.allowed_moves_set.add((blk,None))
        
        for src_blk in self.top_blocks_set:
            for tgt_blk in self.top_blocks_set:
                if not(src_blk == tgt_blk):
                    self.allowed_moves_set.add((src_blk,tgt_blk))

        return

    def allowed_moves(self):
        return self.allowed_moves_set

    def __eq__(self,other):
        if (len(self.blocks_dict) != len(other.blocks_dict)):
            return False
    
        for k in self.blocks_dict:
            if (not(k in other.blocks_dict)):
                return False
            if (not(self.blocks_dict[k] == other.blocks_dict[k]) ):
                return False
        
        for k in other.blocks_dict:
            if (not(k in self.blocks_dict)):
                return False
            if (not(other.blocks_dict[k] == self.blocks_dict[k]) ):
                return False

        return True

    def move(self,from_block,to_block):
        if not ( (from_block,to_block) in self.allowed_moves_set):
            return False

        if (to_block is None):
            above_from,below_from = self.blocks_dict[from_block]
            
            self.blocks_dict[from_block] = (None,None)
            if not(below_from is None):
                u,d = self.blocks_dict[below_from]
                self.blocks_dict[below_from]=(None,d)

                ## Set the top blocks and allowed moves
                ## we have a potentially a new top block in this case
                self.top_blocks_set.add(below_from)
                self.set_allowed_moves()
                # for tblk in self.top_blocks_set:
                #     self.allowed_moves_set.add((tblk,below_from))
                #     self.allowed_moves_set.add((below_from,tblk))

            return True
        else:
            above_from,below_from = self.blocks_dict[from_block]
            above_to,below_to = self.blocks_dict[to_block]
            
            self.blocks_dict[from_block] = (None,to_block)
            self.blocks_dict[to_block] = (from_block,below_to)
            
            if not(below_from is None):
                u,d = self.blocks_dict[below_from]
                self.blocks_dict[below_from] = (None,d)

            ## Set the top blocks and allowed moves
            ## from_block remains in top, new top block is created 
            ## below from and one top block is removed (to_blk)
            if (not(below_from is None)):
                self.top_blocks_set.add(below_from)
                # for tblk in self.top_blocks_set:
                #     self.allowed_moves_set.add((tblk,below_from))
                #     self.allowed_moves_set.add((below_from,tblk))
            self.top_blocks_set.remove(to_block)
            self.set_allowed_moves()
            # rem_list = []
            # for u in self.allowed_moves_set:
            #     if ((u[0] == to_block ) or (u[1] == to_block)):
            #         rem_list.append(u)
            # for u in rem_list:
            #     self.allowed_moves_set.remove(u)

            return True

def next_state(cur_state,move):
    from_block = move[0]
    to_block = move[1]
    next_state = State(blocks_dict=cur_state.blocks_dict,
                       parent = cur_state, 
                       top_blocks_set = cur_state.top_blocks_set,
                       allowed_moves_set = cur_state.allowed_moves_set
                       )
    status = next_state.move(from_block,to_block)
    return next_state

def heuristic_fn(cur_state,goal_state):
    score  =0
    for key in cur_state.blocks_dict:
        u_cur,d_cur = cur_state.blocks_dict[key]
        u_goal,d_goal = goal_state.blocks_dict[key]
        if (d_cur == d_goal):
            score += 1
        else:
            score -= 1

    return score



def simple_hill_climb(src_state, goal_state, heuristic_fn,
                      climb_up =True):
    path = []
    state_scores =[]
    found_goal = False
    stuck_in_minima = False

    if (src_state == goal_state):
        path.append(src_state)
        found_goal = True
        return (found_goal,stuck_in_minima,path,state_scores)
        
    #print(f"state: {cur_state}")

    cur_state = src_state
    while(1):
        #print(f"State:\n{cur_state}")

        if (stuck_in_minima):
            break
        
        path.append(cur_state)
        score = heuristic_fn(cur_state,goal_state)
        state_scores.append(score)
        #print(f"score:{score}")

        if(cur_state == goal_state):
            stuck_in_minima = False
            found_goal = True
            break
         

        ## find a random move
        move_list = list(cur_state.allowed_moves())
        random.shuffle(move_list)
        
        #print(f"allowed_moves = {cur_state.allowed_moves_set}")
        #print(f"move_list: {move_list}")
        stuck_in_minima = True
        
        for m in move_list:
            new_state = next_state(cur_state, m)

            #print(f"move = {m}")
            #print(f"new_state:\n{new_state}")
            
            s_score = heuristic_fn(new_state,goal_state)
            #print(f"new_score:{s_score}")
           
            if (climb_up):
                if (s_score > score):
                     ## we found a higher score state;follow this direction,
                    stuck_in_minima = False
                    cur_state = new_state
                    break
                else:
                    ## continue the search
                    pass 
            else:
                if (s_score < score):
                    ## we found a lower score state;follow this direction, 
                    stuck_in_minima = False
                    cur_state = new_state
                    break
                else:
                    #continue the search
                    pass              
    return (found_goal,stuck_in_minima,path,state_scores)

def trace_path(tstate):
    path = [tstate]
    cur_state =tstate
    while(not (cur_state.parent is None)):
        path.insert(0,cur_state.parent)
        cur_state = cur_state.parent
    return path

def main():
    src_blocks_dict = {}
    #"ADCB" "DCBA"
    src_blocks_dict["A"] = (None,"D")
    src_blocks_dict["D"] = ("A","C")
    src_blocks_dict["C"] = ("D","B")
    src_blocks_dict["B"] = ("C",None)

    goal_blocks_dict = {}
    goal_blocks_dict["D"] =(None,"C")
    goal_blocks_dict["C"] =("D","B")
    goal_blocks_dict["B"] =("C","A")
    goal_blocks_dict["A"] =("B",None)

    src_state = State(src_blocks_dict,None,None,None)
    goal_state = State(goal_blocks_dict,None,None,None)
    found_goal,stuck_in_minima,path,state_scores =simple_hill_climb(src_state,goal_state,heuristic_fn,climb_up=True)

    if (found_goal):
        print("FOUND GOAL")
    if(stuck_in_minima):
        print("STUCK :(")
    print("PATH:")
    for i in range(len(path)):
        print(path[i])
    return
if __name__ == "__main__":
    main()


