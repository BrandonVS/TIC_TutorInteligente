# Generated by Django 4.1.1 on 2022-11-10 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0022_quizusuario_nombre'),
    ]

    operations = [
        migrations.AddField(
            model_name='preguntasrespondidas',
            name='nombreUser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='intentos_username', to='Quiz.quizusuario'),
        ),
    ]
