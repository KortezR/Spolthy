# Generated by Django 4.2.7 on 2023-11-16 10:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_alter_exercise_options_alter_userexercise_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(null=True, verbose_name='Ваш рост')),
                ('weight', models.FloatField(null=True, verbose_name='Ваш вес')),
                ('chest_girth', models.FloatField(null=True, verbose_name='Обхват груди')),
                ('arm_girth', models.FloatField(null=True, verbose_name='Обхват рук')),
                ('waist_girth', models.FloatField(null=True, verbose_name='Обхват талии')),
                ('hip_girth', models.FloatField(null=True, verbose_name='Обхват бедер')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
