from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Recipe, Favorite
from publish_recipe.serializers import RecipeAllSerializer


# Create your views here.
class FavoriteCreateAPIView(generics.GenericAPIView):
    queryset = Recipe.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('pk')
        recipe, created = Favorite.objects.get_or_create(user=user, recipe_id=recipe_id)

        if created:
            return Response({'status': 'Recipe added to favorites.'})
        else:
            return Response({'status': 'Recipe already in favorites.'}, status=status.HTTP_400_BAD_REQUEST)


class FavoriteDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipe_id = self.kwargs.get('pk')
        return Favorite.objects.filter(user=user, recipe_id=recipe_id)

    def delete(self, request, *args, **kwargs):
        user = request.user
        recipe_id = self.kwargs.get('pk')
        try:
            favorite = Favorite.objects.get(user=user, recipe_id=recipe_id)
            favorite.delete()
            return Response({'status': 'Recipe removed from favorites.'})
        except Favorite.DoesNotExist:
            return Response({'status': 'Recipe not in favorites.'}, status=status.HTTP_404_NOT_FOUND)


class UserFavoritesListView(generics.ListAPIView):
    serializer_class = RecipeAllSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        favorite_recipes_ids = Favorite.objects.filter(user=user).values_list('recipe', flat=True)
        return Recipe.objects.filter(id__in=favorite_recipes_ids).prefetch_related('ingredients', 'steps')

