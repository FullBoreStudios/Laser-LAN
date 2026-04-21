from django.contrib import admin

from .models import Arena, BombEvent, BombSite, CombatEvent, Match, MatchPlayer, MatchTeam, Player, Round, RoundPlayerState, Team, TeamMembership, Weapon

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(TeamMembership)
admin.site.register(Arena)
admin.site.register(BombSite)
admin.site.register(Weapon)
admin.site.register(Match)
admin.site.register(MatchTeam)
admin.site.register(MatchPlayer)
admin.site.register(Round)
admin.site.register(RoundPlayerState)
admin.site.register(CombatEvent)
admin.site.register(BombEvent)

# Register your models here.
