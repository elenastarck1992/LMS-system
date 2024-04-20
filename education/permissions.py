from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Класс для роли владельца"""
    message = 'Доступно только владельцам данного контента!'

    def has_object_permission(self, request, view, obj):
        """Метод для проверки принадлежности продукта владельцу"""
        if request.user == obj.owner:
            return True
        return False


class IsModerator(BasePermission):
    """Класс для роли модератора"""
    message = 'Доступно только модераторам!'

    def has_permission(self, request, view):
        if request.user.groups.filter(name='Moderator').exists():
            return True
        return False
