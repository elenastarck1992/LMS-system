from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from education.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    """Тестирование CRUD для уроков"""

    def setUp(self) -> None:
        self.client = APIClient()
        # Создание тестового пользователя
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )
        # Аутентификация тестового пользователя
        self.client.force_authenticate(user=self.user)

        # Создание тестового курса
        self.course = Course.objects.create(
            name="test",
            owner=self.user
        )

        def test_lessons_create():
            """Тестирование создания урока"""

            # Невалидные данные
            data = {
                "name": "test create lesson",
                "lesson_url": "yandex.ru",
                "course": self.course.pk
            }

            response = self.client.post('/lessons/create/', data=data)

            # Проверка статуса
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )
            # Проверка вывода ошибки при вводе невалидных данных
            self.assertEqual(
                response.json(),
                {'lesson_url': ['Запрещено добавлять ссылки на сторонние ресурсы, кроме YouTube']}
            )
            # Проверка наличия записи в БД
            self.assertFalse(Lesson.objects.all().exists())

            # Валидные данные
            data = {
                "lesson_name": "test create lesson",
                "course": self.course.pk,
                "lesson_url": "https://www.youtube.com/watch?v=3g-j-fHUgJ4"
            }

            response = self.client.post('/lesson/create/', data=data)

            # Проверка статуса
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED
            )

            # Проверка создания урока
            self.assertEqual(
                response.json(),
                {"id": 1,
                 "lesson_name": "test create lesson",
                 "description": None,
                 "preview": None,
                 "lesson_url": "https://www.youtube.com/watch?v=3g-j-fHUgJ4",
                 "course": self.course.pk,
                 "owner": self.user.pk}
            )
            # Проверка наличия записи в БД
            self.assertTrue(Lesson.objects.all().exist())

    def test_lesson_list(self):
        """Тестирование получения списка уроков"""
        # Создание тестового урока

        lesson = Lesson.objects.create(
            lesson_name="pagination",
            course=self.course,
            owner=self.user
        )

        response = self.client.get('/lesson/')

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка вывода списка уроков
        self.assertEqual(
            response.json(),
            {"count": 1,
             "next": None,
             "previous": None,
             "results": [
                 {"id": lesson.pk,
                  "lesson_name": lesson.lesson_name,
                  "lesson_description": lesson.lesson_description,

                  "lesson_preview": None,
                  "lesson_url": None,
                  "course": lesson.course_id,
                  "owner": lesson.owner_id}
             ]}
        )

    def test_lesson_retrieve(self):
        """Тестирование получения одного урока"""
        # Создание тестового урока

        lesson = Lesson.objects.create(
            lesson_name="pagination",
            course=self.course,
            owner=self.user
        )

        response = self.client.get(reverse('education:lesson_detail', args=[lesson.pk]))

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        # Проверка вывода одного урока
        self.assertEqual(response.json(),
                         {"id": lesson.pk,
                          "lesson_name": lesson.lesson_name,
                          "lesson_description": lesson.lesson_description,
                          "lesson_preview": None,
                          "lesson_url": None,
                          "course": lesson.course_id,
                          "owner": lesson.owner_id}
                         )

    def test_lesson_update(self):
        """Тестирование изменения урока"""
        # Создание тестового урока

        lesson = Lesson.objects.create(
            lesson_name="pagination",
            course=self.course,
            owner=self.user
        )
        data = {"lesson_name": "validation"}
        response = self.client.patch(reverse('education:lesson_update', args=[lesson.pk]), data=data)

        # Проверка статуса
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

        # Проверка обновления урока
        self.assertEqual(response.json(),
                         {"id": lesson.pk,
                          "lesson_name": "validation",
                          "lesson_description": lesson.lesson_description,
                          "lesson_preview": None,
                          "lesson_url": None,
                          "course": lesson.course_id,
                          "owner": lesson.owner_id}
                         )

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        # Создание тестового урока

        lesson = Lesson.objects.create(
            lesson_name="pagination",
            course=self.course,
            owner=self.user
        )
        response = self.client.delete(reverse('education:lesson_delete', args=[lesson.pk]))

        # Проверка статуса
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)

        # Проверка отсутствия удаленной записи в БД
        self.assertFalse(Lesson.objects.all().exists())


class CourseTestCase(APITestCase):
    """Тестирование CRUD для курсов"""

    def setUp(self) -> None:
        self.client = APIClient()

        # Создание тестового пользователя
        self.user = User.objects.create(
            email="test@test.com",
            password="test",
        )

        # Аутентификация тестового пользователя
        self.client.force_authenticate(user=self.user)

    def test_courses_create(self):
        """Тестирование создания курса"""
        data = {
            "name": 'test create course',
        }
        response = self.client.post('/course/', data=data)

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        # Проверка создания курса
        self.assertEqual(response.json(),
                         {"id": 2,
                          "lesson_list": [],
                          "num_lessons": 0,
                          # "subscribe": None,
                          "name": 'test create course',
                          "preview": None,
                          "description": None,
                          "owner": self.user.pk}
                         )

        # Проверка наличия записи в БД
        self.assertTrue(Course.objects.all().exists())

    def test_courses_list(self):
        """Тестирование получения списка курсов"""

        # Создание тестовых курсов
        course1 = Course.objects.create(
            name='test_course1',
            owner=self.user,
        )

        course2 = Course.objects.create(
            name='test_course2',
            owner=self.user,
        )
        responce = self.client.get('/course/')

        # Проверка статуса
        self.assertEqual(
            responce.status_code,
            status.HTTP_200_OK
        )
        print(responce.json())
        # Проверка вывода списка курсов
        self.assertEqual(
            responce.json(),
            {"count": 2,
             "next": None,
             "previous": None,
             'results': [
                 {"id": course1.pk,
                  "lesson_list": [],
                  "num_lessons": 0,
                  # "subscribe": None,
                  "name": course1.name,
                  "preview": None,
                  "description": None,
                  "owner": self.user.pk},
                 {"id": course2.pk,
                  "lesson_list": [],
                  "num_lessons": 0,
                  # "subscribe": None,
                  "name": course2.name,
                  "preview": None,
                  "description": None,
                  "owner": self.user.pk},
             ]}
        )

    def test_courses_retrieve(self):
        """Тестирование получения одного курса"""

        # Создание тестового курса
        course = Course.objects.create(
            name='test_course',
            owner=self.user
        )

        response = self.client.get(f'/course/{course.id}/')

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка вывода курса
        self.assertEqual(response.json(),
                         {"id": course.pk,
                          "lesson_list": [],
                          "num_lessons": 0,
                          # "subscription": None,
                          "description": course.description,
                          "owner": self.user.pk,
                        "name": course.name,
                          "preview": None}
                         )

    def courses_update(self):
        """Тестирование изменения курса"""
        # Создание тестового курса

        course = Course.objects.create(
            name="test_course",
            owner=self.user
        )
        data = {"name": "test_course_change"}
        response = self.client.patch(reverse("education:courses-detail", args=[course.pk]), data=data)
        print(response.json())

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Проверка обновления курса
        self.assertEqual(
            response.json(),
            {"id": course.pk,
             "lessons_count": [],
             "num_lessons": 0,
             "subscription": None,
             "name": 'test_course_change',
             'preview': None,
             'description': course.description,
             "owner": self.user.pk}
        )

    def test_course_delete(self):
        """Тестирование удаления курса"""
        # Создание тестового курса

        course = Course.objects.create(
            name='test_course',
            owner=self.user
        )

        response = self.client.delete(f'/course/{course.id}/')

        # Проверка статуса
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        # Проверка отсутствия удаленной записи в БД
        self.assertFalse(Course.objects.all().exists())
