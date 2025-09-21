from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import CompetenceLevel, Mission, Prize


class User(AbstractUser):
    experience = models.PositiveSmallIntegerField("Опыт", default=0)
    rank = models.PositiveIntegerField("Ранг", default=1)
    mana = models.PositiveSmallIntegerField("Мана", default=0)

    missions = models.ManyToManyField(Mission, "users", verbose_name="Пройденные миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "users", verbose_name="Имеющиеся уровни компетенций", blank=True
    )

    prizes = models.ManyToManyField(Prize, "users", verbose_name="Полученные призы", blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "notifications", verbose_name="Пользователь")
    text = models.TextField("Текст")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    is_read = models.BooleanField("Прочитано", default=False)

    def __str__(self):
        return f"{self.created_at} - {self.is_read}"

    class Meta:
        verbose_name, verbose_name_plural = "Уведомление", "Уведомления"
        ordering = ["-id"]
