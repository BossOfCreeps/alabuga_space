from django.db import models

from core.models.competence import CompetenceLevel
from core.models.mission import Mission


class Rank(models.Model):
    id = models.PositiveIntegerField("Уровень", primary_key=True)
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Аватар пользователя")

    # условия для получения
    experience = models.PositiveIntegerField("Требуемый опыт")
    missions = models.ManyToManyField(Mission, "ranks_where_required", verbose_name="Обязательные миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "ranks", verbose_name="Требуемые уровни компетенций", blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name, verbose_name_plural = "Ранг", "Ранги"
        ordering = ["id"]
