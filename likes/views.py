from django.shortcuts import render
from rest_framework import status, views, permissions, generics
from rest_framework.response import Response
from .models import Like
from publish_recipe.models import Recipe
from publish_recipe.serializers import RecipeSerializer


# Create your views here.
class LikeAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        recipe = generics.get_object_or_404(Recipe, pk=pk)
        like, created = Like.objects.get_or_create(user=user, recipe=recipe)

        if not created:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'status': 'like added'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        user = request.user
        recipe = generics.get_object_or_404(Recipe, pk=pk)
        like_queryset = Like.objects.filter(user=user, recipe=recipe)
        if like_queryset.exists():
            like_queryset.delete()
            return Response({'status': 'like removed'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'status': 'like not found'}, status=status.HTTP_404_NOT_FOUND)


class LikedRecipesListView(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(likes__user=user)