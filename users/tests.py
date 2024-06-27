from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        """Создание пользователя"""
        self.user = User.objects.create(
            email="test_user@sky.pro",
            password='123qwe',
        )

    def test_create_user(self):
        """Тестирование создания профиля пользователя"""

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('users:user_create'),
            {
                "email": "test@sky.pro",
                "password": "123qwe",
            }
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_list_user(self):
        """Тестирование вывода профилей списка пользователей"""
        self.user = User.objects.create(
            email="admin@sky.pro",
            password='123qwe',
            is_superuser=True,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:user_list')
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_detail_user(self):
        """"Тестирование вывода подробной информации о пользователе"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            reverse('users:user_detail', kwargs={'pk': self.user.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_update_users(self):
        """Тестирование изменения профиля пользователя"""

        updated_data = {
            "telegram_id": "61598870",
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.patch(
            reverse('users:user_update', kwargs={'pk': self.user.id}),
            data=updated_data
        )
        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_user_not_owner(self):
        """
        Тестирование удаления пользователя,
        не являющегося владельцем учетной записи
        """

        new_user = User.objects.create(
            email="test_not_owner@test.ru",
            password="123qwe",
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            reverse('users:user_delete', kwargs={'pk': new_user.id})
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {'detail': 'Вы не являетесь владельцем'}
        )
