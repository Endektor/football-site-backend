from django.db import models
from datetime import date
from django.db.models import Q


class Post(models.Model):   # новость
    title = models.CharField('Заголовок', max_length=255)
    text = models.TextField('Текст')
    createdAt = models.DateField('Дата создания', auto_now_add=True)

    def __str__(self):
        return self.title


class Player(models.Model):
    universal = 'universal'
    midfielder = 'midfielder'
    attack = 'attack'
    defender = 'defender'
    position_choices = [(universal, 'universal'), (midfielder, 'midfielder'),
                        (attack, 'attack'), (defender, 'defender')]
    img = models.ImageField('Аватар', null=True, upload_to='media/api/players/static/images')
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, default='')
    wins_amount = models.IntegerField('Победы', default=0)
    draws_amount = models.IntegerField('Ничьи', default=0)
    defeats_amount = models.IntegerField('Поражения', default=0)
    goals_amount = models.IntegerField('Количество голов', default=0)
    passes_amount = models.IntegerField('Передачи', default=0)
    weight = models.IntegerField('Вес')
    height = models.IntegerField('Рост')
    born_on = models.DateField(verbose_name='Дата рождения', default=date.today)
    position = models.CharField('Позиция', choices=position_choices, default='universal', max_length=255)
    team = models.ForeignKey('Team', verbose_name='Команда', on_delete=models.DO_NOTHING, null=True)
    # оборачиваю Team в кавычки т.к. Team ещё не определен

    def __str__(self):
        return self.first_name


class Team(models.Model):
    img = models.ImageField('Аватар', null=True, upload_to='media/api/teams/static/images')
    name = models.CharField('Название', max_length=255)
    goals_amount = models.IntegerField('Количество голов', default=0)
    miss_amount = models.IntegerField('Пропущенные', default=0)
    wins_amount = models.IntegerField('Победы', default=0)
    draws_amount = models.IntegerField('Ничьи', default=0)
    defeats_amount = models.IntegerField('Поражения', default=0)
    score = models.IntegerField('Счет', default=0)
    difference = models.IntegerField('Разница голов', default=0)
    description = models.TextField('Описание', blank=True, default="")

    def __str__(self):
        return self.name


class Tournament(models.Model):
    img = models.ImageField('Аватар', null=True, upload_to='media/api/tournaments/static/images')
    name = models.CharField('Название', max_length=255)
    members = models.ManyToManyField(Team, verbose_name='Команда', through='Membership', null=True)

    def __str__(self):
        return self.name


class Membership(models.Model):
    team = models.ForeignKey(Team, verbose_name='Команда', on_delete=models.DO_NOTHING)
    tournament = models.ForeignKey(Tournament, verbose_name='Турнир', related_name='member_detail', on_delete=models.DO_NOTHING)
    goals_amount = models.IntegerField('Количество голов', default=0)
    miss_amount = models.IntegerField('Пропущенные', default=0)
    wins_amount = models.IntegerField('Победы', default=0)
    draws_amount = models.IntegerField('Ничьи', default=0)
    defeats_amount = models.IntegerField('Поражения', default=0)
    score = models.IntegerField('Счет', default=0)
    difference = models.IntegerField('Разница голов', default=0)

    def __str__(self):
        return self.team.name + " " + self.tournament.name


class Match(models.Model):
    date = models.DateField(verbose_name='Дата', default=date.today)
    tournament = models.ForeignKey(Tournament, verbose_name='Турнир', on_delete=models.DO_NOTHING)
    team1 = models.ForeignKey(Team, verbose_name='Команда1', related_name='team1', on_delete=models.DO_NOTHING)
    team2 = models.ForeignKey(Team, verbose_name='Команда2', related_name='team2', on_delete=models.DO_NOTHING)
    team1_goals = models.IntegerField('голы команды 1', default=0)
    team2_goals = models.IntegerField('голы команды 2', default=0)

    def __str__(self):
        return self.team1.name + " " + self.team2.name

    def object_update(self, team, goals, miss, wins, draws, defeats):
        team.goals_amount = goals
        team.miss_amount = miss
        team.wins_amount = wins
        team.draws_amount = draws
        team.defeats_amount = defeats
        team.score = wins * 3 + draws
        team.difference = goals - miss
        team.save(update_fields=['goals_amount', 'miss_amount', 'wins_amount',
                                 'draws_amount', 'defeats_amount', 'score', 'difference'])

    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)
        goals, miss, wins, draws, defeats = [0 for i in range(5)]
        matches = Match.objects.all()

        # проходится по матчам, в которых есть команда1 и подсчитывает общее значение. Далее аналогично со второй
        # командой и участниками турниров
        for match in matches.filter(team1=self.team1.id):
            goals += match.team1_goals
            miss += match.team2_goals
            if match.team1_goals > match.team2_goals:
                wins += 1
            elif match.team1_goals == match.team2_goals:
                draws += 1
            else:
                defeats += 1
        for match in matches.filter(team2=self.team1.id):
            goals += match.team2_goals
            miss += match.team1_goals
            if match.team2_goals > match.team1_goals:
                wins += 1
            elif match.team2_goals == match.team1_goals:
                draws += 1
            else:
                defeats += 1
        team = Team.objects.get(id=self.team1.id)
        self.object_update(team, goals, miss, wins, draws, defeats)

        goals, miss, wins, draws, defeats = [0 for i in range(5)]
        for match in matches.filter(team1=self.team2.id):
            goals += match.team1_goals
            miss += match.team2_goals
            if match.team1_goals > match.team2_goals:
                wins += 1
            elif match.team1_goals == match.team2_goals:
                draws += 1
            else:
                defeats += 1
        for match in matches.filter(team2=self.team2.id):
            goals += match.team2_goals
            miss += match.team1_goals
            if match.team2_goals > match.team1_goals:
                wins += 1
            elif match.team2_goals == match.team1_goals:
                draws += 1
            else:
                defeats += 1
        team = Team.objects.get(id=self.team2.id)
        self.object_update(team, goals, miss, wins, draws, defeats)

        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            goals, miss, wins, draws, defeats = [0 for i in range(5)]
            try:
                for match in matches.filter(team1=self.team1.id, tournament=tournament.id):
                    goals += match.team1_goals
                    miss += match.team2_goals
                    if match.team1_goals > match.team2_goals:
                        wins += 1
                    elif match.team1_goals == match.team2_goals:
                        draws += 1
                    else:
                        defeats += 1
                for match in matches.filter(team2=self.team1.id, tournament=tournament.id):
                    goals += match.team2_goals
                    miss += match.team1_goals
                    if match.team2_goals > match.team1_goals:
                        wins += 1
                    elif match.team2_goals == match.team1_goals:
                        draws += 1
                    else:
                        defeats += 1

                membership = Membership.objects.get(team=self.team1.id, tournament=tournament.id)
                self.object_update(membership, goals, miss, wins, draws, defeats)
            except:
                pass

        for tournament in tournaments:
            goals, miss, wins, draws, defeats = [0 for i in range(5)]
            try:
                for match in matches.filter(team1=self.team2.id, tournament=tournament.id):
                    goals += match.team1_goals
                    miss += match.team2_goals
                    if match.team1_goals > match.team2_goals:
                        wins += 1
                    elif match.team1_goals == match.team2_goals:
                        draws += 1
                    else:
                        defeats += 1
                for match in matches.filter(team2=self.team2.id, tournament=tournament.id):
                    goals += match.team2_goals
                    miss += match.team1_goals
                    if match.team2_goals > match.team1_goals:
                        wins += 1
                    elif match.team2_goals == match.team1_goals:
                        draws += 1
                    else:
                        defeats += 1

                membership = Membership.objects.get(team=self.team2.id, tournament=tournament.id)
                self.object_update(membership, goals, miss, wins, draws, defeats)
            except:
                pass