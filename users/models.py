from django.contrib.auth.models import AbstractUser
from django.db import models

from education.models import Course, Lesson


# Create your models here.
class User(AbstractUser):
    """Модель пользователя"""
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email = models.EmailField(unique=True, verbose_name='email')
    phone = models.CharField(max_length=20, verbose_name='номер телефона', null=True, blank=True)
    city = models.CharField(max_length=100, verbose_name='город', null=True, blank=True)
    avatar = models.ImageField(upload_to='media/users_avatar/', null=True, blank=True)

    def __str__(self):
        return f'{self.email} - {self.phone}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'наличные'),
        ('card', 'банковский перевод')
    ]
    """Класс модели платежей"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    payments_date = models.DateTimeField(auto_now=True, verbose_name='дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='оплаченный курс',
                                    null=True, blank=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='оплаченный урок',
                                    null=True, blank=True)
    payment_sum = models.PositiveIntegerField(verbose_name='сумма платежа')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='card',
                                      verbose_name='способ оплаты')
    payment_link = models.URLField(max_length=400, verbose_name='ссылка на оплату', blank=True, null=True)
    payment_id = models.CharField(max_length=255, verbose_name='идентификатор платежа', blank=True, null=True)

    def __str__(self):
        return f'{self.user}: {self.payments_date}, {self.payment_sum}, {self.payment_id}' \
               f'{self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'
        ordering = ['-payments_date']


class Subscription(models.Model):
    """Класс подписки на курс"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='курс')

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
