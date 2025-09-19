from django.contrib import admin

from core.models import (
    Answer,
    Competence,
    CompetenceLevel,
    MissionCode,
    MissionQuiz,
    MissionRecruiting,
    MissionTeaching,
    MissionTree,
    Prize,
    Question,
    Rank,
)


class MissionTreeInline(admin.TabularInline):
    model = MissionTree
    fk_name = "parent"


@admin.register(MissionCode)
class MissionCodeAdmin(admin.ModelAdmin):
    inlines = [MissionTreeInline]


@admin.register(MissionQuiz)
class MissionQuizAdmin(admin.ModelAdmin):
    inlines = [MissionTreeInline]


@admin.register(MissionTeaching)
class MissionTeachingAdmin(admin.ModelAdmin):
    inlines = [MissionTreeInline]


@admin.register(MissionRecruiting)
class MissionRecruitingAdmin(admin.ModelAdmin):
    inlines = [MissionTreeInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
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


@admin.register(Prize)
class PrizeAdmin(admin.ModelAdmin):
    pass
