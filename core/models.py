from django.db import models


class Mission(models.Model):
    class Meta:
        verbose_name, verbose_name_plural = "Миссия", "Миссии"


class Competence(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")

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


class Rank(models.Model):
    id = models.PositiveIntegerField("Уровень", primary_key=True)
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")

    # условия для получения
    experience = models.PositiveIntegerField("Требуемый опыт")
    missions = models.ManyToManyField(Mission, "ranks", verbose_name="Требуемые миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "ranks", verbose_name="Требуемые уровни компетенций", blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name, verbose_name_plural = "Ранг", "Ранги"
        ordering = ["id"]
