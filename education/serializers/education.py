from rest_framework import serializers

from education.models import Course, Lesson
from education.validators import description_validator


class LessonSerializer(serializers.ModelSerializer):
    """Класс сериализатора для урока"""
    link = serializers.CharField(validators=[description_validator], required=False)
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Класс сериализатора для курса"""
    num_lessons = serializers.SerializerMethodField()
    lesson_list = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lesson.objects.filter(course=course).count()
