from django.db import models
from django.conf import settings
from custom_auth.models import CustomUser
from publish_recipe.models import Recipe


class Clash(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    )

    theme = models.CharField(max_length=100)
    initiator = models.ForeignKey(CustomUser, related_name='initiated_clashes', on_delete=models.CASCADE)
    opponent = models.ForeignKey(CustomUser, related_name='received_clashes', on_delete=models.CASCADE, null=True, blank=True)
    winner = models.ForeignKey(CustomUser, related_name='winner_clashes', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    initiator_recipe = models.OneToOneField(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='clash_as_initiator')
    opponent_recipe = models.OneToOneField(Recipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='clash_as_opponent')
    created_at = models.DateTimeField(auto_now_add=True)
