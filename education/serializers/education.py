from rest_framework import serializers

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lesson_list = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lesson.objects.filter(course=course).count()

    def get_lesson_list(self, course):
        """Метод для вывода списка уроков, входящих в курс"""
        return [lesson.lesson_name for lesson in Lesson.objects.filter(course=course)]
