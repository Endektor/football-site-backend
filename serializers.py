from rest_framework import serializers
from .models import Post, Player, Team, Tournament, Membership


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'createdAt')


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'description', 'games_amount', 'goals_amount',
                  'passes_amount', 'weight', 'height', 'age', 'position', 'team')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ('id', 'name', 'games_amount', 'wins_amount', 'draws_amount', 'defeats_amount', 'description')


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'team', 'tournament', 'games_amount', 'wins_amount', 'draws_amount', 'defeats_amount')


class TournamentSerializer(serializers.ModelSerializer):
    member_detail = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'members', 'member_detail')
        depth = 1
