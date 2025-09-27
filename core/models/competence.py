from django.db import models


class Competence(models.Model):
    name = models.CharField("Название", max_length=1024)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Компетенция", "Компетенции"
        ordering = ["id"]


class CompetenceLevel(models.Model):
    competence = models.ForeignKey(Competence, models.CASCADE, "levels", verbose_name="Компетенция")
    level = models.PositiveIntegerField("Уровень")

    def __str__(self):
        return f"{self.competence} - {self.level}"

    class Meta:
        verbose_name, verbose_name_plural = "Уровень компетенции", "Уровни компетенций"
        ordering = ["id"]
