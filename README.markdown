Contains source code for paper presented at ER2010 by Ernst, Borgida, Mylopoulos, Jureta.                                    
                                                                                                                             
Files:                                                                                                                       

* add-text.py -- Uses the [Appscript python framework](http://appscript.sourceforge.net) to interface with OmniGraffle.                                            
* auto-seb.goal -- A file that can be loaded into the [Trento goal modeling tool](http://troposproject.org/tools/grtool/)   
* benchmark.py -- Poor attempt at timing code.
* config.py -- the less said the better.
* convert_omni_seb.py -- draw a model like esp.graffle in Omnigraffle (with the same node attributes) and this script will convert it to a file that can be understood by [Sebastiani's tool](http://github.com/neilernst/goal-reasoning/tree/master/backward_prop/GRTool-Src/Solvers/src/Goalreasoner/lin/Goalsolve/)
* cost_functions.py -- how to prune the options
* display_opt.py -- color options in OmniGraffle using apple script. Good for showing results.
* drive_seb.py -- main driver for the reasoning. START HERE.
* ernst-er-merge.pdf -- the paper.
* examples -- example files, including a graffle model.
* option_parser.py -- given some options, will try to make the best combination of requirements and options.
* a tester for tabu-search algorithm, that doesn't involve painful SAT calls.
