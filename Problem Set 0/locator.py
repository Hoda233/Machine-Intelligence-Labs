from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #TODO: ADD YOUR CODE HERE
    # utils.NotImplemented()

    mySet: Set[Tuple[int,int]] = set()

    # Note: location (x, y) -> (col, row)

    for row_index in range(grid.height):
        for col_index in range(grid.width):
            if grid.__getitem__((col_index,row_index)) == item:
                mySet.add(((col_index,row_index)))

    return mySet




    