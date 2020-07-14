from django.contrib import admin
from .models import Post, Player, TournamentData, Team, Tournament

admin.site.register(Post)
admin.site.register(Player)
admin.site.register(TournamentData)
admin.site.register(Team)
admin.site.register(Tournament)