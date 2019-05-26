###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    ans={}
    file=open(filename,"r")
    while True:
        s=file.readline()
        if len(s)<=0:
            break
        words=s.split(',')
        ans[words[0]]=int(words[1])
    file.close()
    return ans

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    ans=[]
    for v in cows.values():
        if v>limit:
            return ["Can't do this!"]
    cows_copy=cows.copy()
    while len(cows_copy)>0:
        sum=0
        ship=[]
        while sum<limit and len(cows_copy)>0:
            Max=list(iter(cows_copy))[0]
            for k in cows_copy.keys():
                if cows_copy[k]>cows_copy[Max] and sum+cows_copy[k]<=limit:
                    Max=k
            if sum+cows_copy[Max]<=limit:
                ship.append(Max)
                sum+=cows_copy[Max]
                cows_copy.pop(Max)
            else:
                break
        ans.append(ship)
    return ans


# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    partitions=get_partitions(cows.keys())
    for partition in partitions:
        ok=1
        for L in partition:
            sum=0
            for element in L:
                sum+=cows[element]
            if sum>limit:
                ok=0
                break
        if ok:
            return partition

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows=load_cows("ps1_cow_data.txt")
    t=time.time()
    ans1=greedy_cow_transport(cows)
    t=time.time()-t
    print('----------------------------')
    print("greedy cow transport takes %lf seconds."%t)
    print("And the solution to this problem is %d."%len(ans1))

    print('----------------------------')
    t=time.time()
    ans2=brute_force_cow_transport(cows)
    t=time.time()-t
    print("brute force cow transport takes %lf seconds"%t)
    print("And the solution to this problem is %d."%len(ans2))
    print('----------------------------')

compare_cow_transport_algorithms()