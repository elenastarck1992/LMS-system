from rest_framework import serializers

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, course):
        """Метод для подсчета количества уроков, входящих в курс"""
        return Lesson.objects.filter(course=course).count()



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
