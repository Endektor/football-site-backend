from rest_framework import serializers
from .models import Post, Player, Team, Tournament, Membership, Match, Tour, Slide


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'text', 'createdAt', 'logo', 'url')


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


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('id', 'date', 'team1', 'team2', 'team1_goals', 'team2_goals', 'tour')
        depth = 2


class TourSerializer(serializers.ModelSerializer):
    tour_data = MatchSerializer(many=True)

    class Meta:
        model = Tour
        fields = ('id', 'name', 'tournament', 'tour_data')
        depth = 2


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = ('id', 'team', 'tournament', 'goals_amount', 'miss_amount', 'wins_amount',
                  'draws_amount', 'defeats_amount', 'score', 'difference')
        depth = 2


class TournamentSerializer(serializers.ModelSerializer):
    member_detail = MembershipSerializer(many=True, read_only=True)
    tour = TourSerializer(many=True, read_only=True)

    class Meta:
        model = Tournament
        fields = ('id', 'img', 'name', 'url_name', 'members', 'member_detail', 'tour')
        depth = 2


class TournamentNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tournament
        fields = ('id', 'name', 'url_name')


class SlideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slide
        fields = ('id', 'text', 'img', 'url')
