from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from education.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    """Тестирование подписки"""

    def setUp(self) -> None:
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(
            email='test@test.com',
            password='test',
        )
        """Аутентификация тестового пользователя"""
        self.client.force_authenticate(user=self.user)

        # Создание тестового курса
        self.course = Course.objects.create(
            name='test',
            owner=self.user
        )
        print(self.course)

    def test_subscription(self):
        data = {'course_id': self.course.pk}
        response = self.client.post(reverse('users:subscribe'), data=data)
        print(response)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {"message": "подписка добавлена"}
        )

        self.assertTrue(
            Subscription.objects.all().exists()
        )

        response1 = self.client.post(reverse('users:subscribe'), data=data)
        print(response1)
        self.assertEqual(
            response1.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response1.json(),
            {"message": "подписка удалена"}
        )

        self.assertFalse(
            Subscription.objects.all().exists()
        )

