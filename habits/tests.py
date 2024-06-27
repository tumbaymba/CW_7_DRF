from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitsTestCase(APITestCase):
    """Тестирование привычек"""

    def setUp(self):
        """ Создание пользователя и привычек """
        self.user = User.objects.create(
            email="test@sky.pro",
            password='123qwe',
        )

        self.habit = Habit.objects.create(
            owner=self.user,
            place="Выход на работу",
            time="07:00:00",
            action="Выпить стакан воды",
            is_pleasant_habit=False,
            periodicity=1,
            duration=45,
            reward="Любая вкусняшка, но не более 200 Ккал",
            is_public=False,
            related_pleasant_habit=None,
            date=None,
        )

        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        """Тестирование создания привычки"""

        data = {'owner': self.user.id,
                'place': "Дом",
                'time': "19:00:00",
                'action': "Приготовить ужин",
                'is_pleasant_habit': False,
                'periodicity': 1,
                'duration': 90,
                'reward ': "Десерт",
                'is_public': True, }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_update_habits(self):
        """Тестирование изменения привычки"""

        updated_data = {
            "reward": "Протеиновый батончик",
        }

        response = self.client.patch(
            reverse('habits:habit_update', kwargs={'pk': self.habit.id}),
            data=updated_data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_list_habits(self):
        """Тестирование вывода списка привычек"""

        response = self.client.get(
            reverse('habits:habit_list')
        )
        print(response.json())

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {'id': self.habit.id,
                     'place': self.habit.place,
                     'time': self.habit.time,
                     'date': self.habit.date,
                     'action': self.habit.action,
                     'is_pleasant_habit': self.habit.is_pleasant_habit,
                     'periodicity': self.habit.periodicity,
                     'duration': self.habit.duration,
                     'reward': self.habit.reward,
                     'is_public': self.habit.is_public,
                     'owner': self.habit.owner.id,
                     'related_pleasant_habit': self.habit.related_pleasant_habit,
                     }
                ]
            }
        )

    def test_detail_habits(self):
        """Тестирование получения привычки"""

        response = self.client.get(
            reverse('habits:habit_get', kwargs={'pk': self.habit.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_habits(self):
        """Тестирование удаления привычки"""

        response = self.client.delete(
            reverse('habits:habit_delete', kwargs={'pk': self.habit.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_HabitTimeDurationValidator(self):
        """Тестирование невалидного создания привычки.
        Время выполнения должно быть не больше 120 секунд"""

        data = {'owner': self.user.id,
                'place': "Дом",
                'time': "19:00:00",
                'action': "Приготовить ужин",
                'is_pleasant_habit': False,
                'periodicity': 1,
                'duration': 200,
                'reward ': "Десерт",
                'is_public': True, }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время выполнения должно быть не больше 120 секунд']}
        )

    def test_RelatedAndRewardValidator(self):
        """Тестирование невалидного создания привычки.
        Исключить одновременный выбор связанной привычки и указания вознаграждения"""

        data = {'owner': self.user.id,
                'place': "Дом",
                'time': "17:45:00",
                'action': "Приготовить ужин на завтра",
                'is_pleasant_habit': False,
                'periodicity': 1,
                'duration': 75,
                'reward ': "Десерт",
                'is_public': True,
                'related_pleasant_habit': self.habit.id, }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': [
                'Не должно быть заполнено одновременно и поле вознаграждения, и поле связанной привычки. Можно заполнить только одно из двух полей']}

        )

    def test_HabitPleasantValidator(self):
        """Тестирование невалидного создания привычки.
        У приятной привычки не может быть вознаграждения или связанной привычки"""

        data_nice = {'owner': self.user.id,
                     'place': "Дом",
                     'time': "21:00:00",
                     'action': "Сдать ДЗ по учебе",
                     'is_pleasant_habit': True,
                     'periodicity': 2,
                     'duration': 75,
                     'is_public': True,
                     'reward': "Прогуляться",
                     }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data_nice)

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки']}
        )

    def test_CheckHabitValidator(self):
        """Тестирование невалидного создания привычки.
        Нельзя выполнять привычку реже, чем 1 раз в 7 дней.
        За одну неделю необходимо выполнить привычку хотя бы один раз.
        1- каждый день, 2 - через 2 дня, ...7 - раз в неделю"""

        data = {'owner': self.user.id,
                'place': "Дом",
                'time': "19:00:00",
                'action': "Приготовить ужин",
                'is_pleasant_habit': False,
                'periodicity': 8,
                'duration': 100,
                'reward ': "Десерт",
                'is_public': True, }

        response = self.client.post(
            reverse('habits:habit_create'),
            data=data)

        # print(response)

        self.assertEquals(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя выполнять привычку реже, чем 1 раз в 7 дней']}
        )
