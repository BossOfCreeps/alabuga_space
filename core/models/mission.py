from django.db import models

from core.models.competence import CompetenceLevel
from core.models.prize import Prize


class Mission(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")

    rank = models.ForeignKey("Rank", models.CASCADE, "rank_missions", verbose_name="Ранг")
    experience = models.PositiveIntegerField("Опыт")
    mana = models.PositiveIntegerField("Мана")
    prizes = models.ManyToManyField(Prize, "missions", verbose_name="Дает призы", blank=True)
    competence_level = models.ManyToManyField(CompetenceLevel, "missions", verbose_name="Даёт компетенции", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Миссия", "Миссии"
        ordering = ["id"]


class MissionTree(models.Model):
    parent = models.ForeignKey(Mission, models.CASCADE, "as_parent", verbose_name="Корневая миссия")
    child = models.ForeignKey(Mission, models.CASCADE, "as_child", verbose_name="Дочерняя миссия")
