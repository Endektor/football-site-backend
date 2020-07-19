from django.contrib import admin
from .models import Post, Player, Team, Tournament, Membership, Match, Tour, Slide


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class TourInline(admin.TabularInline):
    model = Tour
    extra = 1


class MatchInline(admin.TabularInline):
    model = Match
    extra = 1


class TourAdmin(admin.ModelAdmin):
    inlines = (MatchInline,)


class TeamAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class TournamentAdmin(admin.ModelAdmin):
    inlines = ([MembershipInline, TourInline])


admin.site.register(Post)
admin.site.register(Player)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Membership)
admin.site.register(Match)
admin.site.register(Tour, TourAdmin)
admin.site.register(Slide)
