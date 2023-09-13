from django.shortcuts import render
from .models import Exercise
from urllib.parse import unquote


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    categories = Exercise.EXCERCISE_CATEGORIES
    exercises = Exercise.objects.all()
    return render(request, 'catalog.html', {'exercises': exercises, 'categories': categories})


def exercise(request, exercise_id):
    try:
        e = Exercise.objects.get(id=exercise_id)
    except:
        e = False
    return render(request, 'exercise.html', {'exercise': e})


def search(request):
    try:
        categories = Exercise.EXCERCISE_CATEGORIES
        search = unquote(request.GET['search'])
        exercises = Exercise.objects.filter(name__icontains=search)
        return render(request, 'catalog.html', {'exercises': exercises, 'categories': categories})
    except KeyError:
        return render(request, 'catalog.html')
