from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import AIRecipe
from .serializers import AIRecipeSerializer
from rest_framework import generics, permissions, filters


class AIRecipeListCreateAPIView(generics.ListCreateAPIView):
    queryset = AIRecipe.objects.all().order_by('-date_created')
    serializer_class = AIRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIRecipe.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        user = self.request.user
        if user.AIrecipes.count() >= 10:
            user.awardBake = True
            user.save()


class AIRecipeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AIRecipe.objects.all()
    serializer_class = AIRecipeSerializer


class AIRecipeListView(generics.ListAPIView):
    queryset = AIRecipe.objects.all().order_by('-date_created')
    serializer_class = AIRecipeSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


class AIRecipeDetailView(generics.ListAPIView):
    serializer_class = AIRecipeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AIRecipe.objects.filter(user=self.request.user).order_by('-date_created')