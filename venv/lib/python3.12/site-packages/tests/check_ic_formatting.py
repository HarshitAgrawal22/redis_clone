# -*- coding: utf-8 -*-

#
# IceCream - Never use print() to debug again
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#


import sys
import pprint
from os.path import dirname

sys.path = [dirname(dirname(__file__))] + sys.path
from icecream import ic

ic.configureOutput(includeContext=True)


def multipleMultilineValues():
    d2 = {1: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
          2: 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
          3: 'cccccccccccccccccccccccccccccc',
          4: 'cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc',}

    ic(d2, d2, d2)
#multipleMultilineValues()


ic.configureOutput(prefix='loooooooool| ')

def multilineStrings():
    multilineStr = 'line1\nline2'
    inner = {1: 11111111111111111111111111111111111111111111,
             'multilineStr': multilineStr}
    outer = {1: 11111111111111111111111111111111111111111111,
             'multilineStr': multilineStr,
             'inner': inner}
    #ic(multilineStr)
    ic(outer, 'asdf', 3)
    #print('---')
    #print(pprint.pformat(d).replace('\\n', '\n'))
multilineStrings()


def main():
    for name, value in globals().items():
        if name == 'main' or type(value) is not type(lambda: _): # is not fn
            continue

        fn = value
        print(f'\n== {name}() ==')
        #fn()


if __name__ == '__main__':
    #main()
    pass

