from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserListAPIView, UserDetailAPIView, UserCreateAPIView, UserUpdateAPIView, UserDeleteAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user_detail'),
    path('create/', UserCreateAPIView.as_view(), name='user_create'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),
    path('delete/<int:pk>/', UserDeleteAPIView.as_view(), name='user_delete'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
