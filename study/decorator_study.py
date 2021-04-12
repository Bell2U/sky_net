
# reference: https://www.programiz.com/python-programming/decorator

def star(func):
    def inner(*args, **kwargs):
        print("*" * 30)
        func(*args, **kwargs)
        print("*" * 30)
    return inner


def percent(func):
    def inner(*args, **kwargs):
        print("%" * 30)
        func(*args, **kwargs)
        print("%" * 30)
    return inner


@star
@percent
def printer(msg):
    print(msg)


printer("Hello")



# reference: https://realpython.com/instance-class-and-static-methods-demystified/#delicious-pizza-factories-with-classmethod

class Pizza:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def __repr__(self):
        return f'Pizza({self.ingredients!r})'

    @classmethod
    def margherita(cls):
        return cls(['mozzarella', 'tomatoes'])

    @classmethod
    def prosciutto(cls):
        return cls(['mozzarella', 'tomatoes', 'ham'])

"""Note how I’m using the cls argument in the margherita and prosciutto factory methods 
instead of calling the Pizza constructor directly.

This is a trick you can use to follow the Don’t Repeat Yourself (DRY) principle. 
If we decide to rename this class at some point we won’t have to remember updating the 
constructor name in all of the classmethod factory functions.
"""

# more reference: https://www.programiz.com/python-programming/methods/built-in/classmethod
# this one is more cleanner