from django.urls import path
from .views import LikeAPIView, LikedRecipesListView

urlpatterns = [
    path('recipes/<int:pk>/like/', LikeAPIView.as_view(), name='recipe-like'),
    path('recipes/user/likes/', LikedRecipesListView.as_view(), name='recipe-like'),
]