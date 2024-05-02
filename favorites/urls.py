from django.urls import path
from .views import FavoriteCreateAPIView, FavoriteDestroyAPIView, UserFavoritesListView

urlpatterns = [
    path('recipes/<int:pk>/add_to_favorites/', FavoriteCreateAPIView.as_view(), name='add-to-favorites'),
    path('recipes/<int:pk>/remove_from_favorites/', FavoriteDestroyAPIView.as_view(), name='remove-from-favorites'),
    path('user/favorites/', UserFavoritesListView.as_view(), name='user-favorites'),
]