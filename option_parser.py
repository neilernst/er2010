""" 
Option Parsing for SAT-seb models
Author nernst
Created Feb 9 2010
"""

import time
from pyncomb import ksubsetlex, combfuncs # generate k-subsets

def naive_option(parser, options,   ): 
    """ Given a set of options, create a powerset and try them for admissibility
     Return the sets of options which are admissible or none"""
    valid = {}
    eval_id = 0
    if options == []:
        # run the basic admissibility test
        parser.set_node_ids() #renumber the graph
        parser.generate_seb()
        parser.print_files()
        parser.zero_counts()
        try:
            admissible = parser.run_seb()
        except SebException as se:
                #print "Inadmissible"
                admissible = False
        #print "Admissible: ", admissible
        if admissible:
            valid[eval_id] = 'All Admissible'
        else:
            valid[eval_id] = 'All Inadmissible'
        return valid
    #continue with options if they exist    
    if o_max == None: 
        o_max = len(options)
    if o_min == None: 
        o_min = 0
   #options=g_ids optionset=a subset of g_ids, i.e, a potential soln
    # creates an indexed hash 
    B = combfuncs.createLookup(options)
    if o_max > len(options):
        o_max = len(options)
    option_length = range(o_min, o_max+1)
    option_length.reverse() #start with the largest sets
    for k in option_length:
       # start = time.clock()
        s = ksubsetlex.all(B, k) # s is an iterator over i-th subsets of B with lexicographic ordering
        for optionset in s: # call generator
            if optionset == []:
                break
            print 'optionset is', optionset
            #for o_in in to_include:
                #optionset.append(o_in) # a list of elements the user says must be in the solution                
            eval_id = eval_id + 1
            eval_version = 'option-' + str(eval_id)
            is_subset = False
            for solution in valid.keys(): # don't check subsets of solutions.  #TODO At some point do this efficiently in the powerset generator
                solution = set(valid[solution])
                oset = set(optionset)
                if oset.issubset(solution):
                    is_subset = True
                    break
            if is_subset: 
                continue #with next optionset
            # run the evaluation
            for g_id in optionset: # the graffle ID, immutable
                parser.set_node_status(g_id, 'to_unknown') # change the model so this node is neither optional nor mandatory
            parser.set_node_ids() #renumber the graph
            parser.generate_seb()
            parser.print_files()
            parser.zero_counts()
            try:
                admissible = parser.run_seb()
            except SebException as se:
                for g_id in optionset:
                    parser.set_node_status(g_id, 'to_optional')
                    #print "Inadmissible"
                break
            #print "Admissible: ", admissible
            if admissible:
                valid[eval_version] = optionset
            else:
                valid[eval_version] = 'false'
            # reset the options to T for the next calculation
            for g_id in optionset:
                parser.set_node_status(g_id, 'to_optional')
        #print str(k)+'-subset time taken: ' + str(time.clock() - start)
    # print "valid are:"
    # for v in valid.keys():
    #     print v, ': ',
    #     for o in valid[v]:
    #         print o.name, ',',
    #     print ''
    return valid
    


def tabu_search(candidate, options, attachments):
    """ run tabu search for a local maximal set of options."""
    pass
    
    
def find_solutions(candidate, solutions_list):
    """ input is a list of lists of node-ids
    john's def:
     1. if N subset M, T
     2. if for all n in N, there is an m in M s.t. m preferred n
     3. if M == N
     if any elements are not the same, we can't compare. """
    if techne_parser.prefs == []: 
        return [], solutions_list
    str_prefs = []
    for (g1,g2) in techne_parser.prefs:
        str_prefs.append((str(g1),str(g2)))
    dominators = [] # list of tuples
    i = 0
    for M in solutions_list:
        i += 1
        compare_list = solutions_list[i:] #diagonalized
        for N in compare_list:
            Ms = set(M)
            Ns = set(N)
            # print '\ncost of n is ', calculate_cost(candidate, N), 'cost of M is: ', calculate_cost(candidate, M)
            if Ms == Ns:
                # print str(M) + ' equals ' + str(N)
                dominators.append((M,N))
            elif Ns.issubset(Ms):
                if calculate_cost(candidate, Ns) >= calculate_cost(candidate, Ms):
                    dominators.append((M,N))  
                    # print str(M) + ' superset ' + str(N)
                else: pass#print 'M cost less than N'
            elif Ms.issubset(Ns):
                if calculate_cost(candidate, Ms) >= calculate_cost(candidate, Ns):
                    dominators.append((N,M))
                    # print str(N) + ' superset ' + str(M)
                else: pass#print 'N cost less than M'
            # else:
            #     #neil version of prefs - dominate if any element is preferable
            #     is_dominated = False
            #     for m in Ms:
            #         for n in Ns:
            #             if (m,n) in str_prefs:
            #                 is_dominated = True
            #             if (n,m) in str_prefs:
            #                 is_dominated = False
            #     if is_dominated:
            #     # print str(M) + ' strictly dominates ' + str(N)
            #         dominators.append((M,N))
            else:
                remainderN = Ns - Ms # those elements of N that are not common with M
                remainderM = Ms - Ns # ditto
                is_dominated = True                
                for n in remainderN:
                    for m in remainderM:
                        #print m, n
                        if (m,n) not in str_prefs:
                            is_dominated = False
                if is_dominated:
                    # print str(M) + ' strictly dominates ' + str(N)
                    dominators.append((M,N))

    # we check the set of 'dominators' and get rid of the sets that are transitively dominated e.g. A>B, B>C (but C>A?) 
    # delete solutions that are dominated and not dominant. Circularity implies all are returned. This is not an obj. function (no transitivity)              
    dominant = []
    dominated = []
    #print len(dominators)
    for (A, B) in dominators:
        if A in dominated:
            dominated.remove(A)
        if A not in dominant:
            dominant.append(A)
        if B not in dominant:
            dominated.append(B)
    for element in dominated:
        try:
            solutions_list.remove(element)
        except ValueError: # element already removed
            pass#print 'not in list'
    for element in dominant:
        try:
            solutions_list.remove(element)
        except ValueError: # element already removed
            pass#print 'not in list'
    return dominant, solutions_list
