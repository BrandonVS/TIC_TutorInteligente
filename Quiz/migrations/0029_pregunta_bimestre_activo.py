# Generated by Django 4.1.1 on 2023-01-26 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0028_quizusuario_num_p'),
    ]

    operations = [
        migrations.AddField(
            model_name='pregunta',
            name='bimestre_activo',
            field=models.BooleanField(default=True),
        ),
    ]
