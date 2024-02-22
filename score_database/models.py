from django.db import models
from django.dispatch import receiver




class Team(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

class Score (models.Model):

    time = models.TimeField()
    date = models.DateField()
    round =  models.IntegerField()
    home_team = models.ForeignKey(Team, related_name="home_team",  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_team", on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self) -> str:
        return  self.home_team + self.away_team 

class Weight(models.Model):

    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    score_id = models.ForeignKey(Score, on_delete=models.CASCADE)
    Weight = models.FloatField()

    def __str__(self) -> str:
        return self.score_id
    

class length_database(models.Model):

    date = models.DateField(auto_now=True)
    team_length = models.IntegerField()
    score_length = models.IntegerField()
