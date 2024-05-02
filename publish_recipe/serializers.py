from rest_framework import serializers
from .models import Recipe, Ingredient, Step
from custom_auth.models import CustomUser
import json
from django.core.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    position = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'photo', 'losses', 'wins', 'score', 'first_name', 'last_name', 'position',
                  'awardBurger', 'awardBake', 'top_ten_achievement']
        extra_kwargs = {
            'password': {'write_only': True},
            'wins': {'read_only': True},
            'losses': {'read_only': True},
            'score': {'read_only': True},
            'awardBake': {'read_only': True},
            'awardBurger': {'read_only': True},
            'top_ten_achievement': {'read_only': True},
        }

    def get_position(self, instance):
        users = CustomUser.objects.order_by('-score')

        position = list(users).index(instance) + 1 if instance in users else None

        return position


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['step_text', 'image']


class RecipeCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'serves', 'cook_time', 'description', 'image']


class RecipeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)
    image = serializers.ImageField(use_url=True, required=False, allow_null=True, allow_empty_file=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'serves', 'cook_time', 'description', 'image', 'likes_count', 'ingredients', 'steps']

    def get_likes_count(self, obj):
        return obj.count_likes()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        steps_data = validated_data.pop('steps', [])

        recipe = Recipe.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)

        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)

        return recipe


class RecipeAllSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, required=False)
    steps = StepSerializer(many=True, required=False)
    image = serializers.ImageField(use_url=True, required=False, allow_null=True, allow_empty_file=True)
    likes_count = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'

    def get_likes_count(self, obj):
        return obj.count_likes()