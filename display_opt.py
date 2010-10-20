# -*- coding: utf-8 -*-
from appscript import *

def color_opt(canvas_name='Admissible options'):
    """ Color elements in the given graph with a color indicating optional (orange) or mandatory (coral) """
    graffle = app('OmniGraffle Professional 5')
    doc = graffle.documents[1] # the top document, note 1-indexed array
    s = doc.canvases[canvas_name].get()

    shapes = s.shapes.get()
    graphics = s.graphics.get()
    for element in shapes:
        data = element.user_data.get()
        nodeid = element.id.get()
        if data != None:
            opt = data['optional'] == 'T'
            man = data['mandatory'] == 'T'
            if man: 
                element.fill_color.set((65535,26214,13107)) #orange
            elif opt:
                # set color
                element.fill_color.set((65535,65535,39321)) #'coral'
            else:
                element.fill_color.set((65535,65535,65535))

def set_graph(mands, opts, canvas_name='Admissible options'):
    """ given a list of mandatory and a list of optional node ids, set their data values accordingly."""
    graffle = app('OmniGraffle Professional 5')
    doc = graffle.documents[1] # the top document, note 1-indexed array
    # __s = __doc.canvases['Edits for RE2010'].get()
    s = doc.canvases[canvas_name].get()

    shapes = s.shapes.get()
    graphics = s.graphics.get()
    for element in shapes:
        data = element.user_data.get()
        nodeid = element.id.get()
        if data != None:
            data['mandatory'] = 'F'
            data['optional'] = 'F'
            element.user_data.set(data)
        for el_id in mands:
            if nodeid == el_id:
                data['mandatory'] = 'T'
                data['optional'] = 'F'
                element.user_data.set(data)
        for el_id in opts:
            if el_id == nodeid:
                data['mandatory'] = 'F'
                data['optional'] = 'T'
                element.user_data.set(data)
                
def clear_model(canvas_name='Canvas 1'):
    """ will set all nodes to O: F and M:F """
    graffle = app('OmniGraffle Professional 5')
    doc = graffle.documents[1] # the top document, note 1-indexed array
    # __s = __doc.canvases['Edits for RE2010'].get()
    s = doc.canvases[canvas_name].get()

    shapes = s.shapes.get()
    graphics = s.graphics.get()
    for element in shapes:
        data = element.user_data.get()
        nodeid = element.id.get()
        if data != None:
            data['mandatory'] = 'F'
            data['optional'] = 'F'
            element.user_data.set(data)
                
def get_options(run_id):
    """ return the options and mandatory nodes for the given run number."""
    """
    Run Options Prefs
    0 none/none - baseline time
    1 4 2
    2 6 2
    3 9 2
    4 9 4
    5 12 4
    6 15 4
    7 15 7
    """
    run_id = int(run_id)
    if run_id > 7:
        print run_id
        exit("run_id between 0-7")
    
    mands = [1217,1170,1169] #in every run, satisfy these (FS and -PD)
    
    opts = [
    [] ,                                                                              # run 0 is empty
    [1223,1219,1221,1222] ,                                                           # opts_run1
    [1223,1219,1221,1222,1220,1206] ,                                                 # opts_run2 
    [1223,1219,1221,1222,1220,1206,1207,1376,1186]  ,                                 # opts_run3 
    [1223,1219,1221,1222,1220,1206,1207,1376,1186]  ,                                 # opts_run4 
    [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188]  ,                # opts_run5 
    [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188] ,                 # opts_run6 
    [1223,1219,1221,1222,1220,1206,1207,1376,1186,1189, 1187, 1188,1211, 1213,1204]   # opts_run7 
    ]
    
     #the id of the 2 nodes in the P relation i.e. node1 preferred-to node2 
    prefs = [
    [],
    [(1305, 1306),(1213,1201)] ,                                                                         # prefs_run1 = 
    [(1305, 1306),(1213,1201)]     ,                                                                     # prefs_run2 = 
    [(1305, 1306),(1213,1201)] ,                                                                         # prefs_run3 = 
    [(1305, 1306),(1213,1201),(1204,1211), (1194,1201)] ,                                                # prefs_run4 = 
    [(1305, 1306),(1213,1201),(1204,1211), (1194,1201)] ,                                                # prefs_run5 = 
    [(1305, 1306),(1213,1201),(1204,1211), (1194,1201)] ,                       #softgoals v             # prefs_run6 = 
    [(1305, 1306),(1213,1201),(1204,1211), (1194,1201),(1310,1311),(1311,1312),(1407,1408)]             # prefs_run7 = 
    ]
    
    return mands, opts[run_id], prefs[run_id]
    
if __name__ == '__main__':
    """ set up each run of the experiments. """
    mands, opts, prefs = get_options(1)
    set_graph(mands,opts)
    color_opt()            
    