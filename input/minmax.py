from .Tree import T_Tree
from numba import jit




get_better = lambda val1, val2, state: val2 if state and val1 < val2 or not state and val1 > val2 else val1

    

def compare(values:list, new,  state):

    if state and values[0] < new:

        values[0] = new

    if not state and values[1] > new:

        values[1] = new

    return values


def minmax(tree:T_Tree, values:list, state=True):

    if tree.is_leaf():

        values = compare(values, tree.weight, state)
        return values
    
    for i in tree.children:

        if not i.is_leaf() and state and values[0] < i.weight or not i.is_leaf() and not state and values[1] > i.weight:

            values = compare(values, i.weight, state)
            aux = minmax(i, values, not state)

        else:

            aux = None
            values = values = compare(values, i.weight, state)

        if aux is not None:

            values = compare(values, get_better(aux[0], aux[1], state), state)
        
    return values

