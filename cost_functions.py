def filter_by_prefs(options):
    """ given the preference set, remove options from consideration that are preferred. Note, this is now done 
        before the admissibility is checked, for speed 
        """
    old_options = copy.copy(options)
    options = set(options)
    for (pref, dominated) in tp.prefs:
        for option in options:
            if dominated == option: # we just get rid of it. If a solution isn't found we run again.
                options = options - set([option])
    return list(options), old_options
    
def moop(candidate, options, attachments):
    """ Multi-objective optimization if options contain quantitative values """
    pass
       
def powerset(iterable):
    """ from http://python.org/Documentation/library/itertools.html#recipes"""
    import itertools
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))
 
def find_lowest_cost(cost, increment, dominant, model):
    """ troll through the options and find the lowest cost solution(s). """
    result = []
    # if dominant == []: return dominant
    cost = int(cost)
    increment = int(increment)
    soln_cost_list = []
    # print cost, increment, dominant
    for solution in dominant:
        # print solution, type(model)
        soln_cost = calculate_cost(model, solution)
        soln_cost_list.append((solution, soln_cost))
        # print solution, soln_cost
    while result == []:
        for s in soln_cost_list:    
            if s[1] < cost:
                result.append(s[0])
        cost = cost + increment
    return result

def calculate_cost(model, solution):
    """ go through the list of nodes in a model and calculate a cost """
    total = 0
    for node_id in solution:
        node = techne_parser.find_node(model, node_id)  
        #print node, node.cost, '\n'     
        total = total + node.cost
    return total
    
def option_containment(o_in, o_ex, options_map):
    """ allow user to specify named options by id that must be in solution """
    options_ex = build_options(options, o_ex)
    options_in = build_options(options, o_in)
    options_set = set(options)
    #assuming that the set operations are optimized ...
    result = options_set - options_ex
    result = result - options_in # then re-add to any solutions found
    result = list(result)
    options_in = list(options_in)
    #print "We will look for sets of the following options:", len(result), "+ these mandatory options?: ", options_in
    return result, options_in 
    
    #from http://code.activestate.com/recipes/473878/
def timeout(func, args=(), kwargs={}, timeout_duration=1, default=None):
    '''This function will spwan a thread and run the given function using the args, kwargs and 
    return the given default value if the timeout_duration (in seconds) is exceeded 
    ''' 
    import threading
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*args, **kwargs)
            except:
                self.result = func.results
    it = InterruptableThread()
    it.start()
    it.join(timeout_duration)
    if it.isAlive():
        return it.result
    else:
        return it.result