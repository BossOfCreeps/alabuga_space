from django.db import models


class Prize(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")
    rare = models.PositiveIntegerField("Редкость")
    need_hr_notif = models.BooleanField("Необходимо уведомить HR о получении", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Приз", "Призы"
        ordering = ["-id"]
