from django.contrib import admin

# Register your models here.
from .models import Exercise, UserExercise, Profile

admin.site.register(Exercise)
admin.site.register(UserExercise)
admin.site.register(Profile)
