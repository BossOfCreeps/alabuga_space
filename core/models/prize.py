from django.db import models


class Prize(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")
    rare = models.PositiveIntegerField("Редкость", default=0)
    need_hr_notif = models.BooleanField("Необходимо уведомить HR о получении", default=False)

    price = models.PositiveIntegerField("Цена", default=0, null=True, blank=True)
    is_buying = models.BooleanField("Можно купить в магазине", default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Приз", "Призы"
        ordering = ["-id"]
