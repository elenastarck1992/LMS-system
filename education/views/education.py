import requests
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from education.models import Course, Lesson
from education.paginators import CustomPagination
from education.permissions import IsOwner, IsModerator
from education.serializers.education import CourseSerializer, LessonSerializer
from education.tasks import send_mail_update_course


class CourseViewSet(ModelViewSet):
    """Вьюсет для действий с курсами"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Метод для автоматической привязки курса к создателю"""
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """Метод для запуска функции отправки уведомлений об обновлении курса"""
        update_course = serializer.save()
        send_mail_update_course.delay(update_course.id)
        update_course.save()

    def get_permissions(self):
        """Метод описания доступов к действиям с уроками"""
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    """Класс для создания урока"""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        """Метод для автоматической привязки урока к создателю"""
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """Класс для просмотра списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс для просмотра одного урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс для изменения урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс для удаления урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
