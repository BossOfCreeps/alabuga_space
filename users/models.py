from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import CompetenceLevel, Mission


class User(AbstractUser):
    rank = models.PositiveIntegerField("Ранг", default=1)

    missions = models.ManyToManyField(Mission, "users", verbose_name="Пройденные миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "users", verbose_name="Имеющиеся уровни компетенций", blank=True
    )
