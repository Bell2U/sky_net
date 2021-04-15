# import os, sys, inspect
# current_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# os.chdir(current_dir)
# sys.path.append('../')


# import lib.comms



# another way of doing this
# import sys, os
# find the current executing directory of this py file
# current_dir = sys.path[0]
# print(current_dir)

# find its parent
# parent = os.path.join(current_dir, os.pardir)
# print(parent)
# parent = os.path.realpath(parent)
# print(parent)

# change the current directory to its parent, making module import availble
# sys.path[0] = parent

# test
# from colours import Colour



# lite edition
# import sys, os
# sys.path[0] = os.path.realpath(os.path.join(sys.path[0], os.pardir))

# from colours import Colour