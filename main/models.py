from django.db import models


# Create your models here.
class Exercise(models.Model):

    EXCERCISE_CATEGORIES = [('ch', "грудь"), ('bi', "бицепс"), ('ha', "руки"),
                            ('tr', "трицепс"), ('le', "ноги"), ('sh', "плечи"),
                            ('ca', "кардио"),]

    name = models.CharField(unique=True, max_length=100)
    category = models.CharField(choices=EXCERCISE_CATEGORIES, max_length=2)
    media = models.ImageField(upload_to='media')
    description = models.TextField()
    videolink = models.URLField()
