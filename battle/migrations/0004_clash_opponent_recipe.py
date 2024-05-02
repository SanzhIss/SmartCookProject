# Generated by Django 5.0.3 on 2024-04-08 01:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0003_alter_clash_initiator_recipe'),
        ('publish_recipe', '0003_alter_recipe_image_alter_step_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='clash',
            name='opponent_recipe',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clash_as_opponent', to='publish_recipe.recipe'),
        ),
    ]