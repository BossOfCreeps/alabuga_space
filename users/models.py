from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import CompetenceLevel, Mission, Prize


class User(AbstractUser):
    experience = models.PositiveSmallIntegerField("Опыт", default=0)
    rank = models.PositiveIntegerField("Ранг", default=1)

    missions = models.ManyToManyField(Mission, "users", verbose_name="Пройденные миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "users", verbose_name="Имеющиеся уровни компетенций", blank=True
    )

    balance = models.IntegerField(default=0)
    prizes = models.ManyToManyField(Prize, "users", verbose_name="Полученные призы", blank=True)
