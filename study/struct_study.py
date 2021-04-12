import struct
# reference: https://docs.python.org/3/library/struct.html?highlight=struct#module-struct

def p_up():
    data = 2345676
    p = struct.pack('>I', data)
    print(p, type(p), sep='\n')
    up = struct.unpack('>I', p)
    print(up, type(up), sep='\n')
# p_up()

def byte_obj():
    st = b'1234'
    print(st, type(st), sep='\n')
# byte_obj()

def calcsize_():
    # reference: https://docs.python.org/3/library/struct.html?highlight=struct#format-characters
    data = '2345676'.encode('ascii')
    print(type(data))
    p = struct.pack('>s', data)
    print(struct.calcsize('H'))
    print(struct.calcsize('i'))
# calcsize_()