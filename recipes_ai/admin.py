from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(AIRecipe)
admin.site.register(AIStep)
admin.site.register(AIIngredient)