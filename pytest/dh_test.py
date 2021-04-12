import os, sys, inspect
current_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
os.chdir(current_dir)
sys.path.append('../')

from dh.df import z_star

def z_star_test1():
    n = 21
    zs, phi = z_star(n)
    assert phi == 12
    assert zs == [1, 2, 4, 5, 8, 10, 11, 13, 16, 17, 19, 20]

def f(n) -> int:
    return 4.4

z_star_test1()

a = f(1)
print(type(a))
