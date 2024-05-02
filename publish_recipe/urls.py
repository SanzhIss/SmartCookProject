from django.urls import path
from .views import *

urlpatterns = [
    path('recipes/', RecipeCreateAPIView.as_view(), name='create-recipe'),
    path('my-recipes/', UserRecipeListView.as_view(), name='my-recipes'),
    path('recipes/<int:recipe_id>/ingredients/', IngredientCreateAPIView.as_view(), name='add-ingredient'),
    path('recipes/<int:recipe_id>/steps/', StepCreateAPIView.as_view(), name='add-step'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('all-recipes/', RecipeListView.as_view(), name='all-recipes'),
]