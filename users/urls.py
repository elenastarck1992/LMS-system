from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from .views import MyTokenObtainPairView
from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserRegisterView, UserUpdateView, UserRetrieveView, UserListView, \
    UserDeleteView, SubscriptionAPIView, PaymentsCreate

app_name = UsersConfig.name

urlpatterns = [

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', UserRegisterView.as_view(), name='users-create'),
    path('detail/<int:pk>/', UserRetrieveView.as_view(), name='user-detail'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
    path('course/subscribe/', SubscriptionAPIView.as_view(), name='subscribe'),
    path('payments/create/', PaymentsCreate.as_view(), name='payments-create'),

]
