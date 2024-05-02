from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('register/', views.RegisterUserView.as_view(), name='user_register'),
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('users/all/', views.CustomUserList.as_view(), name='user-list'),
    path('users/<int:pk>/', views.CustomUserDetail.as_view(), name='user-detail'),
    path('password-reset-request/', views.PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', views.PasswordResetCompleteAPIView.as_view(), name='password_reset_confirm'),
    path('users/top/', views.TopUsersByScoreView.as_view(), name='top-users-by-score'),
]
