from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import Exercise, UserExercise, Profile
from urllib.parse import unquote
from .forms import AddExercise, CreateUser, EditUserExercise, EditProfile


def exercise_search(search_name, search_category, exercises):
    if search_category:
        exercises = exercises.filter(category=search_category)
        if exercises:
            exercises = exercises.filter(name__icontains=search_name)
    else:
        exercises = exercises.filter(name__icontains=search_name)
    return exercises


def change_field(new_value):
    if new_value:
        return new_value
    else:
        return None


# Create your views here.
def main_page(request):
    return render(request, 'index.html')


def catalog(request):
    categories = Exercise.EXCERCISE_CATEGORIES
    exercise_ids = []
    if request.user.is_authenticated:

        if request.method == 'POST':
            exercise_id = request.POST['exercise_id']
            exercise_get = Exercise.objects.get(id=exercise_id)
            UserExercise.objects.create(user=request.user, exercise=exercise_get)
            messages.success(request, f'Упражнение "{exercise_get.name}" успешно добавлено на аккаунт')
            return redirect('catalog')
        user_exercises = UserExercise.objects.filter(user=request.user)

        for user_exercise in user_exercises:
            exercise_ids.append(user_exercise.exercise_id)

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
            messages.success(request, f'Упражнение "{e.name.capitalize()}" успешно добавлено на аккаунт')
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
            messages.success(request, f'Упражнение "{name.capitalize()}" успешно добавлено')
            return redirect("catalog")
    else:
        form = AddExercise()
    return render(request, 'add_exercise.html', {'form': form})


def register_user(request):
    if request.user.is_authenticated:
        messages.error(request, 'Для регистрации нового пользователя выйдите с аккаунта')
        return redirect('catalog')
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
        if request.method == 'POST':
            user_exercise_id = request.POST['user_exercise_id']
            user_exercise_get = UserExercise.objects.get(id=user_exercise_id)
            name = user_exercise_get.exercise.name
            user_exercise_get.delete()
            messages.success(request, f'Упражнение "{name.capitalize()}" успешно удалено с аккаунта')
            return redirect('my_exercises')
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

    else:
        return redirect("main_page")
    return render(request, 'my_exercises.html', {'user_exercises': user_exercises, 'categories': categories})


def edit_user_uxercise(request, user_exercise_id):
    if not request.user.is_authenticated:
        messages.error(request, "Вы не авторизованы")
        return redirect('main_page')
    try:
        user_exercise = UserExercise.objects.get(id=user_exercise_id, user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, "Ошибка доступа")
        return redirect('my_exercises')
    if request.method == "POST":
        form = EditUserExercise(request.POST)

        if form.is_valid():
            user_exercise.weight = change_field(request.POST['weight'])
            user_exercise.distance = change_field(request.POST['distance'])
            user_exercise.amount = change_field(request.POST['amount'])
            user_exercise.time = change_field(request.POST['time'])
            user_exercise.save()
            messages.success(request, f'Показатели упражнения "{user_exercise.exercise.name.capitalize()}" успешно изменены')
            return redirect("my_exercises")
    else:
        form = EditUserExercise(instance=user_exercise)
    return render(request, 'edit_user_exercise.html', {'user_exercise': user_exercise, 'form': form})


def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Вы не авторизованы")
        return redirect('main_page')
    try:
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, "Ошибка доступа")
        return redirect('catalog')
    return render(request, 'profile.html', {'user_profile': user_profile})


def edit_profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Вы не авторизованы")
        return redirect('main_page')
    try:
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, "Ошибка")
        return redirect('main_page')
    if request.method == "POST":
        form = EditProfile(request.POST)

        if form.is_valid():
            user_profile.height = change_field(request.POST['height'])
            user_profile.weight = change_field(request.POST['weight'])
            user_profile.chest_girth = change_field(request.POST['chest_girth'])
            user_profile.arm_girth = change_field(request.POST['arm_girth'])
            user_profile.waist_girth = change_field(request.POST['waist_girth'])
            user_profile.hip_girth = change_field(request.POST['hip_girth'])
            user_profile.save()
            messages.success(request, 'Ваш профиль успешно изменен')
            return redirect("profile")
    else:
        form = EditProfile(instance=user_profile)
    return render(request, 'edit_profile.html', {'user_profile': user_profile, 'form': form})
