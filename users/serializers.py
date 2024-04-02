from rest_framework import serializers

from users.models import Payment, User, Subscription


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатора для пользователя"""

    class Meta:
        model = User
        fields = '__all__'


class UserRegisterSerializer(serializers.ModelSerializer):
    """Класс сериализатора для регистрации пользователя"""

    class Meta:
        model = User
        fields = ['email', 'password']


class PaymentsSerializer(serializers.ModelSerializer):
    """Класс сериализатора для платежей"""

    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Класс сериализатора для подписок"""

    class Meta:
        model = Subscription
        fields = '__all__'
