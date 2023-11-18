from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Exercise(models.Model):

    EXCERCISE_CATEGORIES = [('ch', "грудь"), ('bi', "бицепс"), ('ba', "спина"),
                            ('tr', "трицепс"), ('le', "ноги"), ('sh', "плечи"),
                            ('ca', "кардио"),]

    name = models.CharField(unique=True, max_length=100, verbose_name='название')
    category = models.CharField(choices=EXCERCISE_CATEGORIES, max_length=2)
    media = models.ImageField(upload_to='uploads')
    description = models.TextField()

    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'


class UserExercise(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    weight = models.FloatField(null=True, verbose_name='вес')
    distance = models.FloatField(null=True, verbose_name='дистанция')
    amount = models.IntegerField(null=True, verbose_name='повторения')
    time = models.TimeField(null=True, verbose_name='время')

    class Meta:
        verbose_name = 'Упражнение пользователя'
        verbose_name_plural = 'Упражнения пользователей'
        unique_together = ('user', 'exercise',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.FloatField(null=True, verbose_name="Ваш рост")
    weight = models.FloatField(null=True, verbose_name="Ваш вес")
    chest_girth = models.FloatField(null=True, verbose_name="Обхват груди")
    arm_girth = models.FloatField(null=True, verbose_name="Обхват рук")
    waist_girth = models.FloatField(null=True, verbose_name="Обхват талии")
    hip_girth = models.FloatField(null=True, verbose_name="Обхват бедер")
