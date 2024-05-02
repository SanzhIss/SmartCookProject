from rest_framework import serializers
from .models import Clash
from django.utils import timezone
from django.conf import settings
from publish_recipe.models import *
from rest_framework.exceptions import NotFound, PermissionDenied
from publish_recipe.serializers import UserSerializer


class ClashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clash
        fields = ('id', 'theme', 'initiator', 'opponent', 'status')
        read_only_fields = ('status', 'initiator')

    def validate(self, attrs):
        # Check if the initiator or opponent already has a pending or active clash
        user = self.context['request'].user
        opponent = attrs.get('opponent')

        if Clash.objects.filter(initiator=user, status__in=['pending', 'active']).exists():
            raise serializers.ValidationError('You already have an existing or pending clash as an initiator.')

        if Clash.objects.filter(opponent=user, status__in=['pending', 'active']).exists():
            raise serializers.ValidationError('You already have an existing or pending clash as an opponent.')

        if Clash.objects.filter(opponent=opponent, status__in=['pending', 'active']).exists():
            raise serializers.ValidationError('The opponent already has an existing or pending clash.')

        return attrs

    def create(self, validated_data):
        validated_data['initiator'] = self.context['request'].user
        return super().create(validated_data)


class ClashResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clash
        fields = ['status']
        extra_kwargs = {'status': {'write_only': True}}

    def validate_status(self, value):
        # Ensure only "accepted" or "declined" can be set
        if value not in ['accepted', 'declined']:
            raise serializers.ValidationError("Invalid status. Must be either 'accepted' or 'declined'.")
        return value

    def update(self, instance, validated_data):
        # Check if the user is the opponent and if the clash status is pending
        if instance.opponent != self.context['request'].user or instance.status != 'pending':
            raise serializers.ValidationError(
                'You are not authorized to respond to this clash or the clash is not in a pending state.')

        instance.status = validated_data.get('status', instance.status)

        if instance.status == 'accepted':
            instance.start_time = timezone.now()
            instance.end_time = timezone.now() + timezone.timedelta(days=1)

        instance.save()
        return instance


class ClashAddRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clash
        fields = ['initiator_recipe']

    def validate_initiator_recipe(self, value):
        if not value.user == self.context['request'].user:
            raise serializers.ValidationError("You can only add your own recipes to the clash.")
        return value


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = ['id', 'step_text', 'image']


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    steps = StepSerializer(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'user', 'title', 'serves', 'likes_count', 'cook_time', 'description', 'image', 'ingredients', 'steps']
        read_only_fields = ['user']

    def get_likes_count(self, obj):
        return obj.count_likes()

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        steps_data = validated_data.pop('steps')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(recipe=recipe, **ingredient_data)
        for step_data in steps_data:
            Step.objects.create(recipe=recipe, **step_data)
        return recipe


class ClashGetSerializer(serializers.ModelSerializer):
    initiator = UserSerializer(read_only=True)
    opponent = UserSerializer(read_only=True)
    initiator_recipe = RecipeSerializer(read_only=True)
    opponent_recipe = RecipeSerializer(read_only=True)
    winner = UserSerializer(read_only=True)

    class Meta:
        model = Clash
        fields = ['id', 'theme', 'initiator', 'opponent', 'winner', 'status', 'initiator_recipe', 'opponent_recipe', 'created_at']
