# Generated by Django 4.1.1 on 2022-10-10 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0018_alter_quizusuario_puntaje_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='dificultad',
            field=models.IntegerField(null=True, verbose_name='Dificultad pregunta'),
        ),
    ]
