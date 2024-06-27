from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE,
                              verbose_name='пользователь')
    place = models.CharField(max_length=150, **NULLABLE, verbose_name="Место выполнения")
    time = models.TimeField(**NULLABLE, verbose_name="Время начала выполнения", default='12:00:00')
    date = models.DateField(verbose_name='дата', **NULLABLE)
    action = models.CharField(max_length=250, verbose_name="Действие")
    is_pleasant_habit = models.BooleanField(verbose_name="Признак приятной привычки", default=False)
    related_pleasant_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL, **NULLABLE,
                                               verbose_name='связанная(приятная) привычка')
    periodicity = models.IntegerField(default=1, **NULLABLE,
                                      verbose_name='периодичность выполнения привычки для напоминания в днях (по умолчанию ежедневная=1)')
    duration = models.IntegerField(verbose_name='Длительность выполнения, в секундах', **NULLABLE)
    reward = models.CharField(max_length=150, verbose_name='Вознаграждение', **NULLABLE)
    is_public = models.BooleanField(verbose_name='Признак публичности', default=False)

    def __str__(self):
        return f"{self.owner} будет {self.action} (в) {self.time} "

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
