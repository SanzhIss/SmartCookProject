from django.urls import path
from .views import AIRecipeListCreateAPIView, AIRecipeDetailAPIView, AIRecipeListView, AIRecipeDetailView

urlpatterns = [
    path('recipes/ai/', AIRecipeListCreateAPIView.as_view(), name='recipe-list'),
    path('recipes/ai/<int:pk>/', AIRecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('recipes/ai/all/', AIRecipeListView.as_view(), name='all-recipes'),
    path('recipes/ai/user/', AIRecipeDetailView.as_view())

]
