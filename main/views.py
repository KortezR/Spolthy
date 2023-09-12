from django.shortcuts import render
from .models import Exercise


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')


def exercise(request, exercise_id):
    try:
        e = Exercise.objects.get(id=exercise_id)
    except:
        e = False
    return render(request, 'exercise.html', {'exercise': e})
