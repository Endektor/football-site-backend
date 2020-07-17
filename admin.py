from django.contrib import admin
from .models import Post, Player, Team, Tournament, Membership, Match


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class TeamAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class TournamentAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


admin.site.register(Post)
admin.site.register(Player)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Membership)
admin.site.register(Match)
