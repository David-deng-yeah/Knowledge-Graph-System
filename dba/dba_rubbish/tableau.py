'''
    Tablaeu Assistant
    Version: 20201103
'''
#########################################################################
from builtins import hash,print
import time

# private data
_ = {
    'time_init':time.time()  # for performance profiling
}

class main:
#########################################################################
    def __init__(self, dump=False):
        #time_init = time.time()
        _hash = hash(self)
        _[_hash]={}

        #################################################################
        #try:
        #except Exception as ex:
        #    print(ex)

    def __del__(self): _.pop(hash(self), None)
    
#########################################################################
if __name__ == "__main__":
    t = main()
    print(t)
