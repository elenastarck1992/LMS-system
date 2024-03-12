from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для создания суперпользователя"""
    def handle(self, *args, **options):
        user = User.objects.create(
            email='elenovatest@yandex.ru',
            first_name='Elena',
            last_name='Elenova',
            is_staff=True,
            is_superuser=True,
            is_active=True
        )
        user.set_password('12345')
        user.save()
