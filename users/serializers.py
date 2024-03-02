from rest_framework import serializers

from users.models import Payment


class PaymentsSerializer(serializers.ModelSerializer):
    """Класс сериализатора для платежей"""
    class Meta:
        model = Payment
        fields = '__all__'
