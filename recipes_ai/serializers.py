from rest_framework import serializers
from .models import AIRecipe, AIIngredient, AIStep
from publish_recipe.serializers import UserSerializer


class AIIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIIngredient
        fields = ['id', 'name']


class AIStepSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIStep
        fields = ['id', 'step_text',]


class AIRecipeSerializer(serializers.ModelSerializer):
    ingredients = AIIngredientSerializer(many=True, required=False)
    steps = AIStepSerializer(many=True, required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AIRecipe
        fields = '__all__'

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])
        recipe = AIRecipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            AIIngredient.objects.create(recipe=recipe, **ingredient_data)

        for step_data in steps_data:
            step_data.pop('image', None)  # Удалить ключ 'image', если он None
            AIStep.objects.create(recipe=recipe, **step_data)

        return recipe

