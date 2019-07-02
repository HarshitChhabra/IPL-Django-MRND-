from django.db import models

# Create your models here.

class Season(models.Model):
    season = models.IntegerField()

class Matches(models.Model):
    match_id = models.IntegerField()
    season = models.ForeignKey(Season,on_delete=models.CASCADE)
    city = models.CharField(max_length=100,blank=True,null=True)
    date = models.DateField()
    team1 = models.CharField(max_length=100)
    team2 =models.CharField(max_length=100)
    toss_winner =models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=50)
    result = models.CharField(max_length=50)
    dl_applied = models.IntegerField()
    winner = models.CharField(max_length=100,blank=True,null=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=50,blank=True,null=True)
    venue = models.CharField(max_length=200)
    umpire1 = models.CharField(max_length=100,blank=True,null=True)
    umpire2 = models.CharField(max_length=100,blank=True,null=True)
    umpire3 = models.CharField(max_length=100,blank=True,null=True)

class Innings(models.Model):
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    inning_num = models.IntegerField()
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)

class Overs(models.Model):
    inning = models.ForeignKey(Innings,on_delete=models.CASCADE)
    over_number = models.IntegerField()
    bowler = models.CharField(max_length=100)
    is_super_over = models.IntegerField()

class Deliveries(models.Model):
    match_id = models.IntegerField()
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    is_super_over = models.IntegerField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=100,blank=True,null=True)
    dismissal_kind = models.CharField(max_length=100,blank=True,null=True)
    fielder = models.CharField(max_length=100,blank=True,null=True)

#class Delivery_Extra_Data(models.Model):

# class Points(models.Model):
#     team = models.CharField(max_length=200)
#     season = models.ForeignKey(Season,on_delete=models.CASCADE)
#     played = models.IntegerField()
#     won = models.IntegerField()
#     lost =models.IntegerField()
#     points = models.IntegerField()

