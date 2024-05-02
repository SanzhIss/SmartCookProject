from django.urls import path
from .views import (ClashCreateAPIView, ClashResponseAPIView, ClashAddRecipeAPIView, RecipeCreateAPIView,
                    OpponentRecipeCreateAPIView, CurrentUserClashView, EndClashView, UserClashHistoryView,
                    ClashUserListView, OngoingClashesListView)

urlpatterns = [
    path('clashes/create/', ClashCreateAPIView.as_view(), name='clash-create'),
    path('clashes/respond/', ClashResponseAPIView.as_view(), name='clash-respond'),
    path('clashes/initiator/create/', RecipeCreateAPIView.as_view(), name='recipe-create'),
    path('clashes/opponent/create/', OpponentRecipeCreateAPIView.as_view(), name='add-opponent-recipe'),
    path('clashes/current/', CurrentUserClashView.as_view(), name='current-user-clash'),
    path('clashes/<int:pk>/end/', EndClashView.as_view(), name='end-clash'),
    path('user/clash-history/', UserClashHistoryView.as_view(), name='user-clash-history'),
    path('clashes/all', ClashUserListView.as_view(), name='clash-users'),
    path('clashes/ongoing/', OngoingClashesListView.as_view(), name='ongoing-clashes'),
]