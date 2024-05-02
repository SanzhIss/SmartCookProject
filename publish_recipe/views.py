from rest_framework import generics, permissions
from .models import Recipe
from .serializers import *
from .models import Recipe, Ingredient, Step
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView
import json
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


# class RecipeListCreateView(generics.ListCreateAPIView):
#     serializer_class = RecipeSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser, JSONParser]
#
#     def get_queryset(self):
#         user = self.request.user
#         return Recipe.objects.filter(user=user)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

class UserRecipeListView(ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user).order_by('-date_created')


class RecipeCreateAPIView(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        user = self.request.user
        if user.recipes.count() >= 5:
            user.awardBurger = True
            user.save()


class IngredientCreateAPIView(CreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        serializer.save(recipe_id=recipe_id)


class StepCreateAPIView(CreateAPIView):
    queryset = Step.objects.all()
    serializer_class = StepSerializer

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        serializer.save(recipe_id=recipe_id)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]


class RecipeListView(generics.ListAPIView):
    queryset = Recipe.objects.filter(for_clash=False).order_by('-date_created')
    serializer_class = RecipeAllSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']
