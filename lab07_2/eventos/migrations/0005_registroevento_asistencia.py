# Generated by Django 4.2.15 on 2024-10-07 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0004_remove_evento_creador'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroevento',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
    ]
