###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.
    
    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)
    
    Returns: int, smallest number of eggs needed to make target weight
    """
    # TODO: Your code here
    dp=[target_weight]*(target_weight+1)
    dp[0]=0
    dp[1]=1
    for i in range(target_weight+1):
        for egg_weight in egg_weights:
            if i-egg_weight>=0:
                dp[i]=min(dp[i],dp[i-egg_weight]+1)
    
    temp=target_weight
    while temp>0:
        for egg_weight in egg_weights:
            if temp-egg_weight>=0 and dp[temp-egg_weight]+1==dp[temp]:
                memo[egg_weight]=memo.get(egg_weight,0)+1
                temp-=egg_weight
                break
    return dp[target_weight]
    

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    memo={}
    print("Egg weights = (1, 5, 10, 25)")
    print("n = 99")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n,memo))
    print(memo)