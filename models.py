from django.db import models


class Post(models.Model):   # новость
    title = models.CharField('title', max_length=255)
    text = models.TextField('text')
    createdAt = models.DateTimeField('Created at', auto_now_add=True)

    def __str__(self):
        return self.title


class Player(models.Model):
    universal = 'universal'
    midfielder = 'midfielder'
    attack = 'attack'
    defender = 'defender'
    position_choices = [(universal, 'universal'), (midfielder, 'midfielder'),
                        (attack, 'attack'), (defender, 'defender')]
    first_name = models.CharField('First name', max_length=255)
    last_name = models.CharField('Last name', max_length=255)
    description = models.TextField(blank=True, null=True)
    games_amount = models.IntegerField('games', default=0)
    goals_amount = models.IntegerField('goals', default=0)
    passes_amount = models.IntegerField('passes', default=0)
    weight = models.IntegerField('weight')
    height = models.IntegerField('height')
    age = models.IntegerField('age')
    position = models.CharField(choices=position_choices, default='universal', max_length=255)
    team = models.ForeignKey('Team', on_delete=models.DO_NOTHING, null=True, blank=True)
    # оборачиваю Team в кавычки т.к. Team ещё не определен

    def __str__(self):
        return self.first_name


class Team(models.Model):
    name = models.CharField('name', max_length=255)
    games_amount = models.IntegerField('games', default=0)
    wins_amount = models.IntegerField('wins', default=0)
    draws_amount = models.IntegerField('draws', default=0)
    defeats_amount = models.IntegerField('defeats', default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField('name', max_length=255)
    members = models.ManyToManyField(Team, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    tournament = models.ForeignKey(Tournament, on_delete=models.DO_NOTHING)
    games_amount = models.IntegerField('games', default=0)
    wins_amount = models.IntegerField('wins', default=0)
    draws_amount = models.IntegerField('draws', default=0)
    defeats_amount = models.IntegerField('defeats', default=0)

    def __str__(self):
        return self.team.name + " " + self.tournament.name

