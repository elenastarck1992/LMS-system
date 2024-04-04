from rest_framework import serializers

from education.models import Course, Lesson
from education.validators import description_validator
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    """Класс сериализатора для урока"""
    lesson_url = serializers.CharField(validators=[description_validator], required=False)

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Класс сериализатора для курса"""
    num_lessons = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscribe = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lesson.objects.filter(course=course).count()

    def get_subscribe(self, course):
        """Метод для получения данных о наличии подписки на курс у пользователя"""
        user = self.context['request'].user
        for sub in Subscription.objects.filter(course=course):
            if sub.user == user:
                return f'Вы подписаны на обновления этого курса'
