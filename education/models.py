from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='название курса')
    preview = models.ImageField(upload_to='media/course_preview/', verbose_name='превью курса',
                                null=True, blank=True)
    description = models.TextField(verbose_name='описание курса', null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец курса',
                              blank=True, null=True)

    def __str__(self):
        return f'{self.name}: {self.description}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100, verbose_name='название урока')
    lesson_description = models.TextField(verbose_name='описание урока', null=True, blank=True)
    lesson_preview = models.ImageField(upload_to='media/lesson_preview',
                                       verbose_name='изображение урока', null=True, blank=True)
    lesson_url = models.CharField(max_length=300, verbose_name='ссылка на видео',
                                  null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', null=True, blank=True)
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='владелец урока',
                              blank=True, null=True)

    def __str__(self):
        return f'{self.course}: {self.lesson_name} - {self.lesson_description}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'
