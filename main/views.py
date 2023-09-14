from django.shortcuts import render, redirect
from .models import Exercise
from urllib.parse import unquote
from .forms import AddExercise


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    categories = Exercise.EXCERCISE_CATEGORIES
    if request.GET:
        search_name = unquote(request.GET['search'])
        search_category = request.GET.get('category', '')
        if search_category:
            exercises = Exercise.objects.filter(category=search_category)
            if exercises:
                exercises = exercises.filter(name__icontains=search_name)
        else:
            exercises = Exercise.objects.filter(name__icontains=search_name)
    else:
        exercises = Exercise.objects.all()
    return render(request, 'catalog.html', {'exercises': exercises, 'categories': categories})


def exercise(request, exercise_id):
    try:
        e = Exercise.objects.get(id=exercise_id)
    except:
        e = False
    return render(request, 'exercise.html', {'exercise': e})


def add_exercise(request):
    if request.method == "POST":
        form = AddExercise(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("catalog")
    else:
        form = AddExercise()
    return render(request, 'add_exercise.html', {'form': form})
