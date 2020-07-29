from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.views.generic import View
from django.http import HttpResponse
from django.conf import settings
import os

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Player, Team, Tournament, Membership, Match, Tour
from .serializers import *


@api_view(['GET'])
def posts_list(request):
    """
    List of posts.
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        posts = Post.objects.all().order_by('-createdAt')
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = PostSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data,
                         'count': paginator.count,
                         'numpages': paginator.num_pages,
                         'nextlink': '/api/posts/?page=' + str(next_page),
                         'prevlink': '/api/posts/?page=' + str(previous_page)})


@api_view(['GET'])
def posts_detail(request, id):
    """
    Retrieve a post by id.
    """
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def players_list(request):
    """
    List of players.
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        players = Player.objects.all().order_by('id')
        page = request.GET.get('page', 1)
        paginator = Paginator(players, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = PlayerSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        else:
            next_page = page
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data,
                         'count': paginator.count,
                         'numpages': paginator.num_pages,
                         'nextlink': '/api/players/?page=' + str(next_page),
                         'prevlink': '/api/players/?page=' + str(previous_page)})


@api_view(['GET'])
def players_detail(request, id):
    """
    Retrieve a player by id.
    """
    try:
        player = Player.objects.get(id=id)
    except Player.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayerSerializer(player, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def teams_list(request):
    """
    List of teams.
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        teams = Team.objects.all().order_by("score", "difference")
        page = request.GET.get('page', 1)
        paginator = Paginator(teams, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = TeamSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data,
                         'count': paginator.count,
                         'numpages': paginator.num_pages,
                         'nextlink': '/api/teams/?page=' + str(next_page),
                         'prevlink': '/api/teams/?page=' + str(previous_page)})


@api_view(['GET'])
def teams_detail(request, id):
    """
    Retrieve a team by id.
    """
    try:
        team = Team.objects.get(id=id)
        matches = Match.objects.all().filter(team1=id) + Match.objects.all().filter(team1=id)
        matches = matches.order_by("date")
        players_in_team = Player.objects.filter(team=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(team, context={'request': request})
        player_serializer = PlayerSerializer(players_in_team, context={'request': request}, many=True)
        return Response({'data': serializer.data, 'players': player_serializer.data, 'matches': matches.data})


@api_view(['GET'])
def tournaments_list(request):
    """
    List of tournaments.
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        tournaments = Tournament.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(tournaments, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = TournamentSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data,
                         'count': paginator.count,
                         'numpages': paginator.num_pages,
                         'nextlink': '/api/tournaments/?page=' + str(next_page),
                         'prevlink': '/api/tournaments/?page=' + str(previous_page)})


@api_view(['GET'])
def tournaments_detail(request, id):
    """
    Retrieve a tournament by id.
    """
    print(id)
    try:
        tournament = Tournament.objects.get(url_name=id)
    except Tournament.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializered = TournamentSerializer(tournament, context={'request': request})
        return Response({'data': serializered.data})


@api_view(['GET'])
def tournaments_names_list(request):
    """
    List of tournaments names.
    """
    if request.method == 'GET':
        data = []
        tournaments = Tournament.objects.all()
        serializer = TournamentNamesSerializer(tournaments, context={'request': request}, many=True)

        return Response({'data': serializer.data})


@api_view(['GET'])
def memberships_list(request):
    """
    List of memberships.
    """
    if request.method == 'GET':
        data = []
        next_page = 1
        previous_page = 1
        memberships = Membership.objects.all().order_by("score", "difference")
        page = request.GET.get('page', 1)
        paginator = Paginator(memberships, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializer = MembershipSerializer(data, context={'request': request}, many=True)
        if data.has_next():
            next_page = data.next_page_number()
        if data.has_previous():
            previous_page = data.previous_page_number()

        return Response({'data': serializer.data,
                         'count': paginator.count,
                         'numpages': paginator.num_pages,
                         'nextlink': '/api/memberships/?page=' + str(next_page),
                         'prevlink': '/api/memberships/?page=' + str(previous_page)})


@api_view(['GET'])
def memberships_detail(request, id):
    """
    Retrieve a membership by id.
    """
    try:
        membership = Membership.objects.get(id=id)
    except Membership.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MembershipSerializer(membership, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def matches_list(request):
    """
    List of matches.
    """
    if request.method == 'GET':
        matches = Match.objects.all()
        serializer = MatchSerializer(matches, context={'request': request}, many=True)

        return Response({'data': serializer.data})


@api_view(['GET'])
def matches_detail(request, id):
    """
    Retrieve a player by id.
    """
    try:
        match = Match.objects.get(id=id)
    except Match.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MatchSerializer(match, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def slides_list(request):
    """
    List of slides.
    """
    if request.method == 'GET':
        slides = Slide.objects.all()
        serializer = SlideSerializer(slides, context={'request': request}, many=True)

        return Response({'data': serializer.data})


class ReactAppView(View):

    def get(self, request):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        try:
            with open(os.path.join(BASE_DIR, 'frontend', 'build', 'index.html')) as file:
                return HttpResponse(file.read())

        except:
            return HttpResponse(
                """
                index.html not found ! build your React app !!
                """,
                status=501,
            )