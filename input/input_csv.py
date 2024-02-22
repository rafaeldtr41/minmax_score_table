"""
IMPORTANT In order to use the database input method you need to have a database with all the same columns than the
database you share, it doesnt matter if u have more columns, but the columns that have before need to share the same 
names.
"""
import csv
from pathlib import Path
from datetime import datetime
from django.db import IntegrityError
from score_database.models import Team, Score, Weight




format_time = lambda time_str: ':'.join(time_str.split(':')[:2])
format_date = lambda date_string: date_string[:8]


#Returns the object team for relationship
def get_team(name:str):

    try:
        return Team.objects.get(name=name)
    
    except:

        return None

#Insert Score
def insert_score(row:dict):

    
    home_team = get_team(row['home_team'])
    away_team = get_team(row['away_team'])
    
    #This is really weird that happens
    if home_team is None or away_team is None:

        return "Home_team or away_team does not exist"
    
    try:
        aux = Score.objects.create(
            time=datetime.strptime(format_time(row['time']), '%H:%M'),
            date=datetime.strptime(format_date(row['date']), "%d/%m/%y"), 
            home_team=home_team,
            away_team=away_team,
            home_score=int(row['home_score']),
            away_score=int(row['away_score']),
            round=row['round']
            )
        aux.save()
        return "Score Created"
    
    except IntegrityError:

        return "Some fields are None"

def insert_team(name:str):

    try:
        aux = Team.objects.create(name=name)
        aux.save()

    except IntegrityError:

        return "Team " + name + " already exist"

    return "Team " + name + " created"


def open_file(dir:str):

    if not Path(dir).exists():
        
        return "The file not exist"

    file_address = Path(dir)

    try:

        with open(file_address, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            for row in reader:

                print(insert_team(row['home_team']))
                print(insert_team(row['away_team']))
                print(insert_score(row))

    except:

        print(file_address + "is not a csv")


def CalculateWeight():

    Scores = Score.objects.all()
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
