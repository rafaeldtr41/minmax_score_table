from .Tree import T_Tree, get_children
from django.db.models import Q, Subquery
from score_database.models import Weight, Team, Score, MinMax_Weight 
from .minmax import minmax
from numba import jit
from asgiref.sync import sync_to_async
import math




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


def calc_weight(element, state):

    if state:

        return element*1.2
    
    return element


def arm_tree_rec(tree:T_Tree, element, state, id, round):

    if tree.name == id and tree.depth >= round or tree.is_leaf():

        aux = T_Tree(name=element, weight=calc_weight(element.Weight, state), children=[], parent=tree)
        tree.children.append(aux)
            
        return True

    if tree.name == id and tree.depth < round:

        if not tree.is_leaf():

            aux = tree.children

            for i  in aux:

                if not i.is_leaf():

                    return arm_tree(i, element, state)
                
    return False


def arm_tree(team1:str, team2:str, scores):

    try:
        team = Team.objects.get(name=team1)
        against_team = Team.objects.get(name=team2)

    except:

        return " Team dont exists"
    First_Node = T_Tree(name='root', weight=0,children=[], parent=None)
    
    for i in scores:
            
        weight = Weight.objects.get(team_id=team, score_id=i)
        if i.home_team == team.id:

            riv = i.away_team

        else: riv = i.home_team
        state = False

        if not First_Node.is_leaf():

            for j in First_Node.children:

                state = arm_tree_rec(j, weight, riv == against_team.id, riv, i.round)
                if state:
                    break

        if First_Node.is_leaf() or  not state:

            aux = T_Tree(name=riv, weight=calc_weight(weight.Weight, riv == against_team.id), children=[], parent=First_Node)
            First_Node.children.append(aux)
    
    return First_Node
        

    

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
        for j in range(len(teams), i + 1, -1):

            print(j)
            values = minmax(arm_tree(teams[i].name, teams[j -1].name, get_scores(teams[i].id)), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight.objects.create(team_id=teams[i], team_against_id=teams[j - 1], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")

            
            values = minmax(arm_tree(teams[j -1].name, teams[i].name, get_scores(teams[j -1].id)), [-9999999999, 9999999999], state)
            print(values)            
            aux = MinMax_Weight.objects.create(team_id=teams[j -1], team_against_id=teams[i], max_value=values[0], less_value=values[1])
            aux.save()
            print("save 1")
                      

def CalculateWeight(Scores):
    # calc the weight and saves giving a queryset of score
    #Scores = Score.objects.all()
    #Weight for home team
    counter = 0 
    for i in Scores:
        if i.home_score > i.away_score:
            
            val =  math.sqrt(float(i.home_score)*0.1) - math.pow((float(i.away_score)*1.2)*0.1, 2)
            val1 = math.pow((float(i.away_score)*1.2)*0.1, 2)
        
        elif i.home_score == i.away_score:

            val = float(i.home_score)*0.1  
            val1 = (float(i.away_score)*1.2)*0.1
        
        else:

            val = math.pow(float(i.home_score)*0.1, 2)
            val1 = math.sqrt((float(i.away_score)*1.2)*0.1) - math.pow((float(i.home_score)*0.1), 2)
        
        
        home_team = Team.objects.get(id=i.home_team.id)
        away_team = Team.objects.get(id=i.away_team.id)
        aux = Weight.objects.create(
            team_id=home_team,
            score_id=i, 
            Weight=val)
        aux.save()
        #Weight for away team
        
        aux = Weight.objects.create(team_id=away_team, score_id=i, Weight=val1)
        
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


def delete_all():

    #MinMax_Weight_rivals.objects.all().delete()
    MinMax_Weight.objects.all().delete()
    Weight.objects.all().delete()
    Score.objects.all().delete()
    Team.objects.all().delete()

def get_min_max_result(team1:str, team2:str):

    try:

        hteam = Team.objects.get(name=team1)
        ateam = Team.objects.get(name=team2)

    except:

        return "Team dont exists"
    
    aux = MinMax_Weight.objects.filter(team_id=hteam, team_against_id=ateam)
    aux1 = MinMax_Weight.objects.filter(team_id=ateam, team_against_id=hteam)

    return aux.union(aux1)


def get_all_teams():

    return list(Team.objects.all())