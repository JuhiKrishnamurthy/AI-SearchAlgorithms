
import sys
from itertools import permutations

def main():
    src = int(sys.argv[1]) -1
    # denote absense of edge by a value -1
    adj_matrix = [[-1,10,15,20],
                  [10,-1,35,25],
                  [15,35,-1,30],
                  [20,25,30,-1]
                  ]
    other_verts = [v for v in range(0,4) if (not(v == src))]
    
    # other_verts = []
    # for v in range(0,4):
    #     if (not(v == src)):
    #         other_verts.append(v)

    next_permutation=permutations(other_verts)
    min_cost = 10000000
    min_perm = None
    for perm in next_permutation:
        cost = adj_matrix[src][perm[0]]
        for i in range(1,len(perm)):
            edge_src = perm[i-1]
            edge_tgt = perm[i]
            cost += adj_matrix[edge_src][edge_tgt]
        last_ver_in_perm = perm[-1]
        cost += adj_matrix[last_ver_in_perm][src]
        if (cost < min_cost):
            min_cost = cost
            min_perm = perm
    
    path_str = str(src+1)+","
    for v in min_perm:
        path_str += str(v+1)
        path_str += ","
    path_str += str(src+1)

    print("hamiltonian path: " +path_str)
    print("cost = " +str(min_cost))
    return

if __name__ == "__main__":
    main()
    


    


    
    


