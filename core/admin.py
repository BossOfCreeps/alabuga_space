from django.contrib import admin

from core.models import Competence, CompetenceLevel, Mission, Rank


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    pass


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    pass


@admin.register(CompetenceLevel)
class CompetenceLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    pass
