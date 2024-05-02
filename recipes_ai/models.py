from django.db import models
from custom_auth.models import CustomUser


class AIRecipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='AIrecipes', null=True, blank=True)
    title = models.CharField(max_length=100)
    cook_time = models.IntegerField()
    description = models.TextField()
    dish_type = models.CharField(max_length=50)
    serves = models.IntegerField()
    world_cuisine = models.CharField(max_length=50)
    image = models.CharField(max_length=3000, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class AIIngredient(models.Model):
    recipe = models.ForeignKey(AIRecipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


class AIStep(models.Model):
    recipe = models.ForeignKey(AIRecipe, related_name='steps', on_delete=models.CASCADE)
    step_text = models.TextField()
