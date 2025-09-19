from django.contrib import admin

from core.models import Competence, CompetenceLevel, Mission, MissionTree, Prize, Rank


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    class MissionTreeInline(admin.TabularInline):
        model = MissionTree
        fk_name = "parent"

    inlines = [MissionTreeInline]


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    pass


@admin.register(CompetenceLevel)
class CompetenceLevelAdmin(admin.ModelAdmin):
    pass


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    pass


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass
