'''
file: helpers.py
contains helper functions
'''

import os


def count_matrix_pixels(x: int, y: int) -> int:
    return x * y


def clear_screen(): # pragma: no cover
    '''
    clear terminal screen
    '''
    os.system('clear')


def cursor(x=1, y=1, data: str = None):
    '''
    move terminal cursor to position x,y
    and print optional data
    '''
    print('\033[{};{}H{}'.format(x, y, data))
