from .Tree import T_Tree, get_children
from django.db.models import Q, Subquery
from score_database.models import Weight, Team, Score, MinMax_Weight , MinMax_Weight_rivals
from .minmax import minmax
from numba import jit




check_leaves = lambda nodes: None if all(node.is_leaf() for node in nodes) else next((node for node in nodes if not node.is_leaf()), None)
check_pair = lambda x: 1 if x%2 == 0 else -1


def get_Weights(name:str):
# Returns all weights from a team
    try:

        team = Team.objects.get(name=name)

    except:

        return "team not exists"
    
    weight = Weight.objects.filter(team_id=team.id)
    return weight


def get_weight(sid, tid):
# returns weight giving a team and a score
    return Weight.objects.get(score_id=sid, team_id=tid)


def get_scores(team1):
# returns all the scores that a team participates
    return Score.objects.filter(Q(home_team=team1)| Q(away_team=team1))


def get_scores_rivals(team1, team2):
# returns all the scores from a challenge between two teams
    
    return Score.objects.filter(home_team=team1, away_team=team2)


def get_score_one(id:int):
#Return a score giving a id
    try:
        return Score.objects.get(id=id)
    except:

        return None


def get_all_Teams():
# returns all the teams
    return Team.objects.all()



def go_deep(tree:T_Tree, depth:int):
#walk inside a tree until the depth is the desired
    if tree.depth < depth and not tree.is_leaf:

        for j in tree.children:

            if not j.is_leaf():

                return go_deep(j, depth)
            
    if not tree.is_leaf():

        return tree.children[-1]
    
    return tree

def go_deep_inverse_check(tree:T_Tree, depth:int):
#walk inside a tree until the depth is the desired, but the comparison is diferent
    if tree.depth > depth and not tree.is_leaf:

        for j in tree.children:

            if not j.is_leaf():

                return go_deep(j, depth)
            
    if not tree.is_leaf():

        return tree.children[-1]
    
    return tree


def arm_tree(team01:str, team02:str,scores, state=True ):
#Arm the tree so it can be evaluated
    
    #get team against
    try:
        #get the teams
        team1:Team = Team.objects.get(name=team01)
        team2:Team = Team.objects.get(name=team02)
    except:
        return "team not exists"
    
    #First Node Init
    First_Node = T_Tree(name=0, weight=-99999999999, parent=None)
    # init the returning tree
    # if team not added create node with punctuation, 
    # else add new weight as children
    # if depth < round add node as children and go lower
    # else add new children to central
    
    for i in scores:

        #sign = check_pair(float(i.round))
        if i.home_team == team1.id:
            # check if is away or home
            riv = i.away_team
            weight = get_weight(i.id, i.home_team)

        else:

            riv = i.home_team
            weight = get_weight(i.id, i.away_team)

        if riv == team2.id:
            # check if the rival is the element on the list
            val = 1.1#*sign
        
        else: val = 1#*sign

        if not First_Node.is_leaf():

            # asign a children with the name desired
            get_val = get_children(riv,First_Node, 1, 0)
            
            
            if get_val is not None:
                #if exists
                if  i.round < get_val.depth:
                    # if is more deep than the actual val
                    get_val = go_deep(i, i.round)

                
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


def arm_tree_inverse(team01:str, team02:str,scores, state=True ):
    #the same but the deepness is treated diferently
    
    #get team against
    try:
        
        team1:Team = Team.objects.get(name=team01)
        team2:Team = Team.objects.get(name=team02)
    except:
        return "team not exists"
    
    #First Node Init
    First_Node = T_Tree(name=0, weight=-99999999999, parent=None)
    scores.order_by("-round")
    # if team not added create node with punctuation, 
    # else add new weight as children
    # if depth < round add node as children and go lower
    # else add new children to central
    
    for i in scores:

        #sign = check_pair(float(i.round))
        if i.home_team == team1.id:

            riv = i.away_team
            weight = get_weight(i.id, i.home_team)

        else:

            riv = i.home_team
            weight = get_weight(i.id, i.away_team)

        if riv == team2.id:
            
            val = 1.1#*sign
        
        else: val = 1#*sign

        if not First_Node.is_leaf():

            
            get_val = get_children(riv,First_Node, 1, 0)
            
            
            if get_val is not None:
                
                if  i.round > get_val.depth:

                    get_val = go_deep(i, i.round)

                
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
    # to print the tree, WARNING, the trees are to big, this would take a time, a serious time
    print("Init node:" + str(tree.name) + " weight: " + str(tree.weight) + "Childrens: \n")

    for i in tree.children: 
        
        
        if i.is_leaf():

            print("node:" + str(i.name) + " weight: " + str(i.weight) + "Childrens: \n")
        
        else: 

            aux = ""
            state = True
            lista = i
            while state:
                
                leaf_childrens = ""
                if state:
                    
                    aux = aux + leaf_childrens + "node:" + str(lista.name) + " weight: " + str(lista.weight) + "Childrens: \n"
                else:

                    aux = aux + leaf_childrens
                
                state = False

                for j in lista.children:

                    if  not j.is_leaf():

                        state = True
                        lista = j

                    else:

                        leaf_childrens = leaf_childrens + "node:" + str(j.name) + " weight: " + str(j.weight) + "Childrens: \n"
                    
            print(aux)


    

def get_new_scores():
    #returns the new scores added
    aux = Weight.objects.only('score_id').all()

    try:

        return Score.objects.filter(id__in=Subquery(aux)).order_by('round')

    except:

        return "Error getting the scores"
    

def calculate_all(state):
    # apply the minmax to the trees
    teams = Team.objects.all()
    print("here")
    print(len(teams))
    for i in range(0, len(teams)):
        print(i)
        for j in range(16, i + 1, -1):

            print(j)
            values = minmax(arm_tree(teams[i].name, teams[j -1].name,get_scores(teams[i].id)  ,state), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight.objects.create(team_id=teams[i], team_against_id=teams[j - 1], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")

            
            values = minmax(arm_tree(teams[j -1].name, teams[i].name, get_scores(teams[j -1].id)  ,state), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight.objects.create(team_id=teams[j -1], team_against_id=teams[i], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")
                      


def calculate_only_rivals(state):
    #apply the minmax to the trees but the trees only contain values from the rival teams
    teams = Team.objects.all()
    print("here")
    print(len(teams))
    for i in range(0, len(teams)):
        print(i)
        for j in range(16, i + 1, -1):

            print(j)
            values = minmax(arm_tree(teams[i].name, teams[j -1].name, get_scores_rivals(teams[i].id, teams[j -1 ].id),  state), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight_rivals.objects.create(team_id=teams[i], team_against_id=teams[j - 1], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")

            
            values = minmax(arm_tree(teams[j -1].name, teams[i].name, get_scores_rivals(teams[j -1 ].id, teams[ i ].id),  state), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight_rivals.objects.create(team_id=teams[j -1], team_against_id=teams[i], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")


def CalculateWeight(Scores):
    # calc the weight and saves giving a queryset of score
    #Scores = Score.objects.all()
    #Weight for home team
    counter = 0 
    for i in Scores:
        
        val = i.home_score  +  (float(i.away_score)*-1.2)
        home_team = Team.objects.get(id=i.home_team.id)
        away_team = Team.objects.get(id=i.away_team.id)
        aux = Weight.objects.create(
            team_id=home_team,
            score_id=i, 
            Weight=val)
        aux.save()
        #Weight for away team
        val = val*-1  
        aux = Weight.objects.create(team_id=away_team, score_id=i, Weight=val)
        
        aux.save()
        counter +=2
        print("Inserted two")
        print(counter)


def calculate_new_weight():

    # silly func to call after adding new values.
    try:
        aux = Weight.objects.only('team_id').all()
        CalculateWeight(Score.objects.filter(id__in=Subquery(aux)))
    
    except:

        CalculateWeight(Score.objects.all())
    

def delete_all_min_max():
    # delete all minmax values. IMPORTANT, if u add new values you need to calc the minmax again
    MinMax_Weight.objects.all().delete()


def delete_all_weight():
    #delete all weight
    Weight.objects.all().delete()


