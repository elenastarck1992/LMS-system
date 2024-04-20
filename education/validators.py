from rest_framework import serializers


def description_validator(value):
    if 'youtube.com' not in value:
        raise serializers.ValidationError('Запрещено добавлять ссылки на сторонние ресурсы, кроме YouTube')
