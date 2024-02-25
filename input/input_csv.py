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
import re




format_time = lambda time_str: ':'.join(time_str.split(':')[:2])
lambda_date = lambda date_string: date_string[:8]
lambda_date1 = lambda date_string: date_string[4:]

MONTH = {'Jan':"1", "Feb":"2", "Mar":"3", "Apr":"4", "May":"5", "Jun":"6", "Jul":"7", "Aug":"8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12" }

#Returns the object team for relationship
def get_team(name:str):

    try:
        return Team.objects.get(name=name)
    
    except:

        return None
    

def format_date(string:str):

    regex_format_conv = re.compile(r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(\d{2})")
    regex_format_day_week = re.compile(r"(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}")

    if regex_format_conv.search(string):

        
        return datetime.strptime(lambda_date(string), "%d/%m/%y")
    
    if regex_format_day_week.search(string):

        aux = string.split(' ')

        string = aux[2] + "/" + MONTH[aux[1]] + "/" + aux[3][2:]
        print(string)
        try:
            return datetime.strptime(string, "%d/%m/%y")

        except:

            return datetime.strptime("01/12/22", "%d/%m/%y")
    



#Insert Score
def insert_score(row:dict):

    
    home_team = get_team(row['home_team'])
    away_team = get_team(row['away_team'])
    
    #This is really weird that happens
    if home_team is None or away_team is None:

        return "Home_team or away_team does not exist"
    
    try:
        aux = Score.objects.create(
            #time=datetime.strptime(format_time(row['time']), '%H:%M'),
            date=format_date(row["date"]), 
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

    #try:

    with open(file_address, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            for row in reader:

                print(insert_team(row['home_team']))
                print(insert_team(row['away_team']))
                print(insert_score(row))

    #except:

     #   print(file_address + "is not a csv")
