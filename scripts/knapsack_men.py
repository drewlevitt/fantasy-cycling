import pandas as pd
import time
import random

# Create all_riders DataFrame
men = pd.read_csv('../data/FSA_DS_Men2019.csv')
men = men[['Rider Name', 'Price', 'Score 2019']]
men['24+'] = (men['Price'] >= 24).astype(int)
men['18+'] = (men['Price'] >= 18).astype(int)

# Create a mini DataFrame for fast(er) testing
men_mini = men[(men['Score 2019'] > 0) & (men.index % 10 == 0)]
men_mini

def knapsack_men(to_consider, avail, memo={}):
    # to_consider is a tuple of rider indices
    # avail is a tuple of (points remaining to spend, 24+ point slots remaining, 18+ point slots remaining, all slots remaining)
    # we're also going to query a global 'men' DataFrame variable, bite me
    
    if (to_consider, avail) in memo:
        result = memo[(to_consider, avail)]
    elif to_consider == () or avail[0] == 0 or avail[3] == 0:
        result = (0, ())
    else:
        next_rider = men.loc[to_consider[0]]
        if (next_rider['Price'] > avail[0]) or (next_rider['24+'] > avail[1]) or (next_rider['18+'] > avail[2]):
            #Explore right branch only
            result = knapsack_men(to_consider[1:], avail, memo)
        else:
            #Explore left branch
            with_avail = (avail[0] - next_rider['Price'],
                          avail[1] - next_rider['24+'],
                          avail[2] - next_rider['18+'],
                          avail[3] - 1)
            with_val, with_team = knapsack_men(to_consider[1:], with_avail, memo)
            with_val += next_rider['Score 2019']
            #Explore right branch
            without_val, without_team = knapsack_men(to_consider[1:], avail, memo)
            #Choose better branch
            if with_val > without_val:
                result = (with_val, with_team + (to_consider[0],))
            else:
                result = (without_val, without_team)
    memo[(to_consider, avail)] = result
    return result

shuffled_mini = tuple(random.sample(list(men_mini.index), len(men_mini.index)))
t0 = time.perf_counter()
val, taken = knapsack_men(shuffled_mini, (150, 1, 3, 25))
t1 = time.perf_counter()
print(val, taken)
print('{} seconds elapsed'.format(t1-t0))
print('Spent {} points on {} riders'.format(men_mini[men_mini.index.isin(taken)]['Price'].sum(), 
                                            len(men_mini[men_mini.index.isin(taken)])))
print(men_mini[men_mini.index.isin(taken)])