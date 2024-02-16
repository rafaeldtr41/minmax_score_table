from django.db import models
from django.dispatch import receiver




class Team(models.Model):

    name = models.CharField(max_length=255, unique=True)


class Score (models.Model):

    time = models.DateTimeField()
    date = models.DateField()
    round =  models.IntegerField()
    home_team = models.ForeignKey(Team, related_name="home_team",  on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_team", on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()


class Weight(models.Model):

    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    score_id = models.ForeignKey(Score, on_delete=models.CASCADE)
    Weight = models.FloatField()


""" ----------------------------------------Triggers-----------------------------------------------------------------------------"""

@receiver(models.signals.post_save, sender=Score)
def CalculateWeight(sender, **kwargs):

    #Weight for home team
    val = sender.home_score  +  (sender.away_score * -1.2)
    aux = Score.objects.create(sender.home_team, sender, val)
    aux.save()
    #Weight for away team
    val = val * -1
    aux = Score.objects.create(sender.away_team, sender, val)




