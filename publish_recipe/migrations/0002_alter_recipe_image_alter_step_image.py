# Generated by Django 5.0.3 on 2024-04-04 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publish_recipe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='step',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
