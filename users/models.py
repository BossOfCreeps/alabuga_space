from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import CompetenceLevel, Mission, Prize, Rank


class User(AbstractUser):
    experience = models.PositiveIntegerField("Опыт", default=0)
    rank = models.PositiveIntegerField("Ранг", default=1)
    mana = models.PositiveIntegerField("Мана", default=0)

    missions = models.ManyToManyField(Mission, "users", verbose_name="Пройденные миссии", blank=True)
    competence_level = models.ManyToManyField(
        CompetenceLevel, "users", verbose_name="Имеющиеся уровни компетенций", blank=True
    )

    prizes = models.ManyToManyField(Prize, "users", verbose_name="Полученные призы", blank=True)
    theme = models.CharField("Тема", max_length=10, default="light")

    invite_users = models.PositiveIntegerField("Число приглашённых пользователей", default=0)
    is_hr = models.BooleanField("HR", default=False)

    def competence_level_map(self):
        return {o.competence_id: o.level for o in self.competence_level.all()}

    def check_next_rank(self):
        next_rank = Rank.objects.filter(id=self.rank + 1).first()
        if not next_rank:
            return

        user_cl_map, has_competence_level = {o.competence_id: o.level for o in self.competence_level.all()}, True
        for next_rank_cl in next_rank.competence_level.all():
            if user_cl_map.get(next_rank_cl.competence_id, 0) < next_rank_cl.level:
                has_competence_level = False
                break

        if (
            self.experience >= next_rank.experience
            and (set(next_rank.missions.values_list("pk")).issubset(set(self.missions.values_list("pk"))))
            and has_competence_level
        ):
            self.rank = next_rank.id
            self.save()


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


class Journal(models.Model):
    user = models.ForeignKey(User, models.CASCADE, "journals", verbose_name="Пользователь")
    text = models.TextField("Текст")
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.user}"

    class Meta:
        verbose_name, verbose_name_plural = "Запись в журнале", "Записи в журнале"
        ordering = ["-id"]
