from django.contrib import admin

from education.models import Course, Lesson
from users.models import User, Payment


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение списка пользователей"""
    list_display = ('phone', 'email')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Отображение списка платежей"""
    list_display = ('user', 'payments_date', 'paid_course', 'paid_lesson')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Отображение списка курсов"""
    list_display = ('name', 'preview', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Отображение списка уроков"""
    list_display = ('lesson_name', 'lesson_description', 'lesson_preview', 'course')
