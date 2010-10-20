""" test tabu search """
from convert_omni_seb import ParseQGM
from display_opt import clear_model, set_graph
from pyncomb import ksubsetlex, combfuncs # generate k-subsets
import copy
import random 
import config

def is_admissible(optlst):
    """ an oracle. given a set of options, determine admissibility. Simulate Seb reasoning."""
    #admissible =     D,         C,           A,      AC,                CD
    optset = set(optlst)
    admissible = [set([1223]), set([1219]), set([1207]), \
                  set([1207,1219]), set([1219,1223]), set([1207, 1223,1186]),set([1207, 1219,1186]), set([1223,643,1186,1207]), set([1223,1219,1186,1207])]
    # admissible_harder = [set([1223]),  set([1219]), set([1223,1186]), set([1223,1186,1207]), set([1223,1219,1186,1207])]
    if optset in admissible:
        return True
    return False
        
def set_up():
    """ generate an example from ESP """
    # using test-tabu canvas from esp.graffle
    opts1 = [1223,1207,1219,1214]
    opts2 = [1223,1219,1221,1222,1220,1206]                                                 # opts_run2 
    opts3 = [1223,1219,1221,1222,1220,1206,1207,1376,1186]                                 # opts_run3 
    opts5 = [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188]                # opts_run5 
    opts15 = [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188,1211, 1213,1204]
    opts7 = [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188,1211, 1213,1204,988,765,655,643,333] #15
    mands = [1217,1169]
    model = []
    tlim = 400 #seconds
    
    test_comb(opts2, 4, 8)
    #config.checks = 0
    
    #tabu_search(None, opts1, tlim) 
    print 'made ', config.checks, 'checks'
    


def test_comb(options,o_min, o_max, to_include=None ):
    """ the naive approach """
    config.checks = 0
    if o_max == None: 
        o_max = len(options)
    if o_min == None: 
        o_min = 0
    if to_include == None:
        to_include = []
    #options=g_ids optionset=a subset of g_ids, i.e, a potential soln
     # creates an indexed hash 
    B = combfuncs.createLookup(options)
    if o_max > len(options):
        o_max = len(options)
    option_length = range(o_min, o_max+1)
    #option_length = range(len(options))
    option_length.reverse() #start with the largest sets
    # generate powersets
    for k in option_length:
        s = ksubsetlex.all(B, k) # s is an iterator over i-th subsets of B with lexicographic ordering
        for optionset in s: # call generator
            for o_in in to_include:
                optionset.append(o_in) # a list of elements the user says must be in the solution
            ad = is_admissible(optionset)
            config.checks += 1
            if ad:
                #pass
                print optionset, " admissible"
                
    print 'made ', config.checks, 'checks'
                
def tabu_search(model, opts, tlim):
    candidate = []
    config.time = 0
    config.expire = 20
    config.solution = []
    config.tabu_list = []    
    config.tlim = tlim
    while config.time < tlim and candidate not in config.tabu_list:
        tmp = copy.copy(opts)
        tabu_move([], tmp)
        if config.time % config.expire <= 1:# every 20 cycles
            config.tabu_list = []
    print 'solution', config.solution
    
def tabu_move(candidate, remainder):
    # a given iteration
    # take the current list of options that are an admissible set
    step = 0
    radius = len(remainder)
    selected = None
    tmp_c = []
    config.time += 1
    initial = len(candidate)
    tmp_r = copy.copy(remainder)
    while step < radius:
        tmp_c = copy.copy(candidate)
        if tmp_r == []:
            break
        selected = random.choice(tmp_r)
        step += 1
        tmp_c.append(selected)
        if selected not in config.tabu_list and tmp_c not in config.solution:
            break       
        else:
            tmp_r.remove(selected) # prevent reconsideration of this element
            tmp_c.remove(selected)
    if len(tmp_c) == initial:
        # we didn't find one to add
        if set(candidate) not in config.solution:
            config.solution.append(set(candidate)) 
        return # BASE CASE
        
    remainder.remove(selected) 
    candidate.append(selected)
    if config.time > config.tlim:
        return
        
    ad = is_admissible(candidate)
    config.checks += 1
    if ad:
        tabu_move(candidate, remainder) # RECURSE and go up a level and if nothing, store the solution
    else:
        candidate.remove(selected) # off into the ether
        remainder.append(selected)
        if selected not in config.tabu_list:
            config.tabu_list.append(selected)
        tabu_move(candidate, remainder) # RECURSE to same level
    return 

def subset(candidate, solution):
    """ see if a given set is a subset of existing solutions """
    setC = set(candidate)
    for soln in solution:
        set_soln = set(soln)
        if setC <= set_soln: #subset
            return True
    return False
    
def main():
    """ """
    # soln = run_tabu(options, model, tlim)
    assert(True)


           
if __name__ == '__main__':
    set_up()
    main()