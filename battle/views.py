from rest_framework import generics, status
from .serializers import ClashSerializer, ClashResponseSerializer, ClashAddRecipeSerializer, ClashGetSerializer
from rest_framework.generics import UpdateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from publish_recipe.models import *
from publish_recipe.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Clash
from django.db.models import Q, F
from django.db import transaction
from django.utils import timezone


class ClashCreateAPIView(generics.CreateAPIView):
    queryset = Clash.objects.all()
    serializer_class = ClashSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)


class ClashResponseAPIView(UpdateAPIView):
    queryset = Clash.objects.all()
    serializer_class = ClashResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            clash = Clash.objects.get(opponent=self.request.user, status='pending')
        except Clash.DoesNotExist:
            raise NotFound("No pending Clash found where you are the opponent.")
        return clash

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class ClashAddRecipeAPIView(UpdateAPIView):
    queryset = Clash.objects.all()
    serializer_class = ClashAddRecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        clash = super().get_queryset().get(pk=self.kwargs['pk'], initiator=self.request.user)
        if clash.status != 'pending':
            raise ValidationError("You can only add recipes to pending clashes.")
        return clash


# class RecipeCreateAPIView(CreateAPIView):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         clash = Clash.objects.filter(initiator=self.request.user, status='pending').order_by('-created_at').first()
#         if not clash:
#             raise ValidationError('No pending clash found for this user.')
#
#         recipe = serializer.save(user=self.request.user)
#
#         clash.initiator_recipe = recipe
#         clash.save()


class RecipeCreateAPIView(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        clash = Clash.objects.filter(initiator=self.request.user, status='pending').order_by('-created_at').first()
        if not clash:
            raise ValidationError('No pending clash found for this user.')

        recipe = serializer.save(user=self.request.user, for_clash=True)

        clash.initiator_recipe = recipe
        clash.save()


class OpponentRecipeCreateAPIView(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        clash = Clash.objects.filter(opponent=self.request.user, status='accepted').order_by('-created_at').first()
        if not clash:
            raise ValidationError('No pending clash found for this user.')

        recipe = serializer.save(user=self.request.user, for_clash=True)

        clash.opponent_recipe = recipe
        clash.save()


class CurrentUserClashView(ListAPIView):
    serializer_class = ClashGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Clash.objects.filter(
            models.Q(initiator=user) | models.Q(opponent=user),
            models.Q(status='pending') | models.Q(status='accepted')
        ).distinct()


class EndClashView(APIView):

    def post(self, request, pk, format=None):
        clash = get_object_or_404(Clash, pk=pk)

        if clash.status not in ['pending', 'accepted']:
            return Response({'error': 'Clash is not in a state that can be ended.'}, status=400)

        with transaction.atomic():
            initiator_likes = clash.initiator_recipe.likes.count()
            opponent_likes = clash.opponent_recipe.likes.count()

            if initiator_likes > opponent_likes:
                clash.winner = clash.initiator
                winner = clash.initiator
                loser = clash.opponent
                winner.wins += 1
                loser.losses += 1
                winner.score += 50
                loser.score += 5
            elif opponent_likes > initiator_likes:
                clash.winner = clash.opponent
                winner = clash.opponent
                loser = clash.initiator
                winner.wins += 1
                loser.losses += 1
                winner.score += 50
                loser.score += 5
            else:
                clash.initiator.score += 25
                clash.opponent.score += 25

            clash.status = 'completed'
            clash.save()

            clash.initiator.save(update_fields=['score'])
            clash.opponent.save(update_fields=['score'])

            top_ten_users = CustomUser.objects.order_by('-score')[:10]
            if winner in top_ten_users:
                winner.top_ten_achievement = True
            else:
                winner.top_ten_achievement = False
            winner.save(update_fields=['top_ten_achievement'])

            if loser in top_ten_users:
                loser.top_ten_achievement = True
            else:
                loser.top_ten_achievement = False
            loser.save(update_fields=['top_ten_achievement'])

        return Response({'message': 'Clash ended and winner determined.'})


class UserClashHistoryView(ListAPIView):
    serializer_class = ClashGetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Clash.objects.filter(
            Q(initiator=user) | Q(opponent=user),
            status='completed'
        ).order_by('-created_at')


class ClashUserListView(ListAPIView):
    queryset = Clash.objects.all()
    serializer_class = ClashGetSerializer


class OngoingClashesListView(ListAPIView):
    serializer_class = ClashGetSerializer
    queryset = Clash.objects.filter(status='accepted')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     username = self.request.query_params.get('username', None)
    #     if username is not None:
    #         queryset = queryset.filter(Q(initiator__username=username) | Q(opponent__username=username))
    #     return queryset


