# Generated by Django 5.0.3 on 2024-04-08 01:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('battle', '0002_clash_initiator_recipe'),
        ('publish_recipe', '0003_alter_recipe_image_alter_step_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clash',
            name='initiator_recipe',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clash_as_initiator', to='publish_recipe.recipe'),
        ),
    ]
