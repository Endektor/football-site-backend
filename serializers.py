from rest_framework import serializers
from .models import Post, Player, Team, Tournament, Membership, Match


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'createdAt')


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'img', 'first_name', 'last_name', 'patronymic', 'wins_amount', 'draws_amount',
                  'defeats_amount', 'goals_amount', 'passes_amount', 'weight', 'height', 'born_on',
                  'position', 'team')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'img', 'name', 'goals_amount', 'miss_amount', 'wins_amount',
                  'draws_amount', 'defeats_amount', 'score', 'difference', 'description')


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'team', 'tournament', 'goals_amount', 'miss_amount', 'wins_amount',
                  'draws_amount', 'defeats_amount', 'score', 'difference')


class TournamentSerializer(serializers.ModelSerializer):
    member_detail = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'members', 'member_detail')
        depth = 1


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('id', 'date', 'tournament', 'team1', 'team2', 'team1_goals', 'team2_goals')
