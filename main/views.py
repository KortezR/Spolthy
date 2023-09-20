from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Exercise, UserExercise
from urllib.parse import unquote
from .forms import AddExercise, CreateUser


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    categories = Exercise.EXCERCISE_CATEGORIES
    exercise_ids = []
    if request.user.is_authenticated:
        user_exercises = UserExercise.objects.filter(user=request.user)
        for user_exercise in user_exercises:
            exercise_ids.append(user_exercise.exercise_id)
        if request.method == 'POST':
            exercise_id = request.POST['exercise_id']
            exercise_get = Exercise.objects.get(id=exercise_id)
            UserExercise.objects.create(user=request.user, exercise=exercise_get)
            messages.success(request, f'Упражнение "{exercise_get.name}" успешно добавлено на аккаунт')
    if request.GET:
        exercises = exercise_search(unquote(request.GET['search']),
                                    request.GET.get('category', ''),
                                    Exercise.objects.all())
    else:
        exercises = Exercise.objects.all()
    return render(request, 'catalog.html', {'exercises': exercises, 'categories': categories, 'exercise_ids': exercise_ids})


def exercise(request, exercise_id):
    try:
        e = Exercise.objects.get(id=exercise_id)
    except:
        e = False
    if request.user.is_authenticated:
        user_exercise = UserExercise.objects.get(user=request.user, exercise=e)
        if user_exercise:
            user_has = True
        else:
            user_has = False
        if request.method == 'POST':
            UserExercise.objects.create(user=request.user, exercise=e)
            messages.success(request, 'Упражнение успешно добавлено на аккаунт')
            user_has = True
    else:
        user_has = False
    return render(request, 'exercise.html', {'exercise': e, 'user_has': user_has})


def add_exercise(request):
    if request.method == "POST":
        form = AddExercise(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            name = form.cleaned_data['name']
            messages.success(request, f'Упражнение "{name}" успешно добавлено')
            return redirect("catalog")
    else:
        form = AddExercise()
    return render(request, 'add_exercise.html', {'form': form})


def register_user(request):
    if request.method == "POST":
        form = CreateUser(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Пользователь {username} успешно создан')
            return redirect("login")
    else:
        form = CreateUser()
    return render(request, 'register.html', {'form': form})


def my_exercises(request):
    categories = Exercise.EXCERCISE_CATEGORIES
    if request.user.is_authenticated:
        user_exercises = UserExercise.objects.filter(user=request.user)
        if request.GET:
            get_exercises = []
            for user_exercise in user_exercises:
                get_exercises.append(user_exercise.exercise.id)
            exercises = Exercise.objects.filter(id__in=get_exercises)
            exercises = exercise_search(unquote(request.GET['search']),
                                        request.GET.get('category', ''),
                                        exercises)
            user_exercises = user_exercises.filter(exercise__in=exercises)
    return render(request, 'my_exercises.html', {'user_exercises': user_exercises, 'categories': categories})


def exercise_search(search_name, search_category, exercises):
    if search_category:
        exercises = exercises.filter(category=search_category)
        if exercises:
            exercises = exercises.filter(name__icontains=search_name)
    else:
        exercises = exercises.filter(name__icontains=search_name)
    return exercises
