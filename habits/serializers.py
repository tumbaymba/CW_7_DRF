from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitTimeDurationValidator, RelatedAndRewardValidator, \
    HabitRelatedHabitIsPleasantValidator, HabitPleasantValidator, CheckHabitValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        validators = [
            RelatedAndRewardValidator(field1='related_pleasant_habit', field2='reward'),
            HabitTimeDurationValidator(field='duration'),
            HabitRelatedHabitIsPleasantValidator(field1='related_pleasant_habit', field2='is_pleasant_habit'),
            HabitPleasantValidator(field1='related_pleasant_habit', field2='reward', field3='is_pleasant_habit'),
            CheckHabitValidator(field='periodicity')
        ]
        fields = '__all__'


class HabitPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ('action', 'place', 'time', 'periodicity', 'duration', 'related_pleasant_habit', 'reward',)
