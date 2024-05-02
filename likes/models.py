from django.db import models
from django.conf import settings
from publish_recipe.models import Recipe
from custom_auth.models import CustomUser


# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='liked_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.email} likes {self.recipe.title}"

