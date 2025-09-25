from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from polymorphic.models import PolymorphicModel

from core.models.competence import CompetenceLevel
from core.models.prize import Prize


class Mission(PolymorphicModel):  # условно абстрактный класс
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение")

    rank = models.IntegerField("Ранг")
    experience = models.PositiveIntegerField("Опыт")
    mana = models.PositiveIntegerField("Мана")
    prizes = models.ManyToManyField(Prize, "missions", verbose_name="Дает призы", blank=True)
    competence_level = models.ManyToManyField(CompetenceLevel, "missions", verbose_name="Даёт компетенции", blank=True)

    def do_success(self, user):
        user.missions.add(self)
        user.journals.create(
            text=f"Пользователь прошёл миссию {self.name} (+{self.experience} опыта, +{self.mana} маны)"
        )
        user.experience += self.experience
        user.mana += self.mana

        for prize in self.prizes.all():
            user.prizes.add(prize)
            if prize.need_hr_notif:
                user.notifications.create(text=f"Пользователь получил артефакт {prize.name}")
                user.journals.create(text=f"Получен артефакт {self.name}")

        user_cl_map = {o.competence_id: o.level for o in user.competence_level.all()}
        for cl in self.competence_level.all():
            if cl.competence_id not in user_cl_map:
                user_cl_map[cl.competence_id] = cl.level
            else:
                user_cl_map[cl.competence_id] += cl.level

        user.competence_level.clear()
        for c_id, level in user_cl_map.items():
            user.competence_level.add(CompetenceLevel.objects.get_or_create(competence_id=c_id, level=level)[0])

        user.save()
        user.check_next_rank()

    def type_data(self) -> str:
        raise NotImplementedError

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Миссия", "Миссии"
        ordering = ["id"]


class MissionTree(models.Model):
    parent = models.ForeignKey(Mission, models.CASCADE, "as_parent", verbose_name="Корневая миссия")
    child = models.ForeignKey(Mission, models.CASCADE, "as_child", verbose_name="Дочерняя миссия")


class MissionCode(Mission):
    code = models.CharField("Код", max_length=1024, unique=True)

    mission_type = "Квест"

    def type_data(self) -> str:
        return f"Код: {self.code}"

    def verify(self, user, code: str):
        v = self.rank == user.rank and self.code == code and self not in user.missions.all()
        if v:
            self.do_success(user)
        return v

    class Meta:
        verbose_name, verbose_name_plural = "Миссия Квест", "Миссии Квест"
        ordering = ["id"]


class MissionRecruiting(Mission):
    invited = models.PositiveIntegerField("Сколько необходимо пригласить")

    mission_type = "Рекрутинг"

    def type_data(self) -> str:
        return f"Нужно пригласить: {self.invited}"

    class Meta:
        verbose_name, verbose_name_plural = "Миссия Рекрутинг", "Миссии Рекрутинг"
        ordering = ["id"]


class MissionTeaching(Mission):
    content = CKEditor5Field(config_name="extends")

    def type_data(self) -> str:
        return f"Длина html: {len(self.content)}"

    mission_type = "Лекторий"

    class Meta:
        verbose_name, verbose_name_plural = "Миссия Лекторий", "Миссии Лекторий"
        ordering = ["id"]


class MissionQuiz(Mission):
    questions = models.ManyToManyField("Question", "missions", verbose_name="Вопросы")

    def type_data(self) -> str:
        return f"Кол-во вопросов: {self.questions.count()}"

    mission_type = "Симулятор"

    class Meta:
        verbose_name, verbose_name_plural = "Миссия Симулятор", "Миссии Симулятор"
        ordering = ["id"]


class Question(models.Model):
    name = models.CharField("Название", max_length=1024)
    description = models.TextField("Описание")
    file = models.FileField("Файл", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name, verbose_name_plural = "Вопрос", "Вопросы"
        ordering = ["id"]


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.question} - {self.text}"

    class Meta:
        verbose_name, verbose_name_plural = "Ответ", "Ответы"
        ordering = ["id"]
