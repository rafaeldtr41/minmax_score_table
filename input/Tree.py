





class  T_Tree():

    def __init__(self, name:int=0, weight:float=0, children:list=[], parent=None, depth:int=0) -> None:
        
        self.name = name
        self.weight = weight
        self.children = children
        self.parent = parent
        self.depth = depth

    def is_leaf(self):

        return len(self.children) == 0
    
    def is_root(self):

        return self.parent is None
    
    def __str__(self):

        return "Node: " +  str(self.name) + " childrens: " + str(self.children)

    def delete_children(self, name):

        for i in self.children:

            if i.name == name:

                self.children.remove(self.children.index(i))

def get_children(name, tree:T_Tree, depth=99999999999999, actual_depth=0):

        if actual_depth < depth:
            
            if tree.name == name:

                return tree

            for i in tree.children:

                if not i.is_leaf():

                    actual_depth +=1
                    return get_children(name, i, depth, actual_depth)
                
                else:

                    if i.name == name:

                        return i
        else:
            return None        


def get_childrens(tree, depth=99999999999, actual_depth=0):

    if actual_depth < depth:
            
            for i in tree.children:

                if not i.is_leaf():

                    actual_depth +=1
                    return get_childrens( i, depth, actual_depth)
    
        
    elif depth == actual_depth:
            
            return tree.children

    else: return None       
