from rest_framework.exceptions import ValidationError
from habits.models import Habit

class RelatedAndRewardValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_pleasant_habit = value.get(self.field1)
        reward = value.get(self.field2)

        if related_pleasant_habit and reward:
            raise ValidationError(
                'Не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей')


class HabitTimeDurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        field_value = value.get(self.field)

        if field_value is not None and int(field_value) > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд')

class HabitRelatedHabitIsPleasantValidator:

    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        related_pleasant_habit = value.get(self.field1)
        is_pleasant_habit = value.get(self.field2)

        if is_pleasant_habit == True:
            if related_pleasant_habit:
                raise ValidationError(
                    'Связанной привычкой может быть только приятная привычка. В связанные привычки могут попадать только привычки с признаком приятной привычки')


class HabitPleasantValidator:

    def __init__(self, field1, field2, field3):
        self.field1 = field1
        self.field2 = field2
        self.field3 = field3

    def __call__(self, value):
        related_pleasant_habit = value.get(self.field1)
        reward = value.get(self.field2)
        is_pleasant_habit = value.get(self.field3)

        if is_pleasant_habit == True:
            if related_pleasant_habit or reward:
                raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки')


class CheckHabitValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        periodicity = value.get(self.field)

        if periodicity is not None and ((periodicity > 7) or (periodicity < 1)):
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней')

