import math

def minkowski_dist(src_array, tgt_value_pos_dict, p):
    ## for each value in src_array, find where it is in the target
    ## compute the distance and sum

    ##the blank tile value is 0, 
  
    dist = 0
    for y in range(0,3):
        for x in range(0,3):
            val = src_array[y][x]
            tgt_pos = tgt_value_pos_dict[val]
            dist += math.pow(abs(y - tgt_pos[1]),p)
            dist += math.pow(abs(x - tgt_pos[0]),p)
    
    dist = math.pow(dist,1.0/float(p))
    return dist

def manhattan_dist(src_array, tgt_value_pos_dict):
    man_dist = minkowski_dist(src_array, tgt_value_pos_dict, 1.0)
    return man_dist

def euclidean_dist(src_array, tgt_value_pos_dict):
    euclid_dist = minkowski_dist(src_array, tgt_value_pos_dict, 2.0)
    return euclid_dist

def main():
    #compute the distance between two configurations with various distance metrics

    src_array = [[2,0,3],[1,8,4],[7,6,5]]
    tgt_array = [[1,2,3],[8,0,4],[7,6,5]]

    ## value of p for minkowski dist
    p = 0.5

    ## create tgt value_pos dict
    tgt_value_pos_dict={}
    for y in range(0,3):
        for x in range(0,3):
            val = tgt_array[y][x]
            tgt_value_pos_dict[val] = (x,y)
    
    euclid_dist = euclidean_dist(src_array, tgt_value_pos_dict)
    man_dist = manhattan_dist(src_array, tgt_value_pos_dict)
    mink_dist = minkowski_dist(src_array, tgt_value_pos_dict, p)

    print("euclid_dist = " +str(euclid_dist))
    print("manhattan_dist = " +str(man_dist))
    print("minkowski_dist = " +str(mink_dist))

    return

if __name__ == "__main__":
    main()
    