from django.db import models
from custom_auth.models import CustomUser


class Recipe(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    serves = models.PositiveSmallIntegerField()
    cook_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipes_images/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    for_clash = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def count_likes(self):
        return self.likes.count()


class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    step_text = models.TextField()
    image = models.ImageField(upload_to='steps_images/', null=True, blank=True)

    def __str__(self):
        return self.recipe.title
