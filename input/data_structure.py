from .Tree import T_Tree, get_children
from django.db.models import Q
from score_database.models import Weight, Team, Score




check_leaves = lambda nodes: None if all(node.is_leaf() for node in nodes) else next((node for node in nodes if not node.is_leaf()), None)
check_pair = lambda x: 1 if x%2 == 0 else -1


def get_Weights(name:str):

    try:

        team = Team.objects.get(name=name)

    except:

        return "team not exists"
    #Returns all the weight from a team union with Score to access home or away team and round, also order by round    
    weight = Weight.objects.filter(team_id=team.id)
    return weight


def get_weight(sid, tid):

    return Weight.objects.get(score_id=sid, team_id=tid)


def get_scores(team1):

    return Score.objects.filter(Q(home_team=team1)| Q(away_team=team1))


def get_score_one(id:int):

    try:
        return Score.objects.get(id=id)
    except:

        return None


def get_all_Teams():

    return Team.objects.all()



def go_deep(tree:T_Tree, depth:int):

    if tree.depth < depth and not tree.is_leaf:

        for j in tree.children:

            if not j.is_leaf():

                return go_deep(j, depth)
            
    return tree

def arm_tree(team01:str, team02:str, state=True):

    
    #get team against
    try:
        
        team1 = Team.objects.get(name=team01)
        team2 = Team.objects.get(name=team02)
    except:
        return "team not exists"
    
    #First Node Init
    First_Node = T_Tree(name=0, weight=-99999999999, parent=None)
    scores = get_scores(team1.id)
    # if team not added create node with punctuation, 
    # else add new weight as children
    # if depth < round add node as children and go lower
    # else add new children to central
    
    for i in scores:

        sign = check_pair(float(i.round))
        if i.home_team == team1.id:

            riv = i.away_team
            weight = get_weight(i.id, i.home_team)

        else:

            riv = i.home_team
            weight = get_weight(i.id, i.away_team)

        if riv == team2.id:
            
            val = 2*sign
        
        else: val = 1*sign

        if not First_Node.is_leaf():

            
            get_val = get_children(riv,First_Node, 1, 0)
            
            
            if get_val is not None:
                
                if  i.round < get_val.depth:

                    aux = T_Tree(name=riv, weight=weight.Weight*val, parent=get_val,depth=get_val.depth+1)
                    lista = []
                    lista.append(T_Tree(name=riv, weight=weight.Weight*-val, parent=aux))
                    aux.children = lista
                    lista = get_val.children
                    lista.append(aux)
                    get_val.children = lista

                else:
                    
                    aux = T_Tree(name=riv, weight=weight.Weight*val, parent=get_val, depth=get_val.depth+1)
                    lista = get_val.children
                    lista.append(aux)
                    get_val.children = lista

            else:           
                aux = T_Tree(name=riv, weight=weight.Weight*val, parent=First_Node, depth=First_Node.depth+1)
                lista = First_Node.children
                lista.append(aux)
                First_Node.children = lista
        
        else:
                
                aux = T_Tree(name=riv, weight=weight.Weight*val, parent=First_Node, depth=First_Node.depth+1)
                lista = First_Node.children
                lista.append(aux)
                First_Node.children = lista

    return First_Node


def wide_walk_str(tree:T_Tree):

    if tree.is_leaf(): 
        
        return "\n node: " + str(tree.name)

    string = "node: " + str(tree.name)  + "childrens \n"   
    for i in tree.children:

        if not i.is_leaf():

             aux_string = "" + wide_walk_str(i)

        else:
            aux_string = ""

        string =  string + "node: " + str(i.name) + ","

    return string + aux_string 