"""
URL configuration for Spolthy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from main import views as main_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.main_page, name='main_page'),
    path("catalog/", main_views.catalog, name='catalog'),
    path('exercises/<int:exercise_id>/', main_views.exercise, name='exercise'),
    path('exercises/add/', main_views.add_exercise, name='add_exercise'),
    path('accounts/register', main_views.register_user, name='register'),
    path('my_exercises/', main_views.my_exercises, name='my_exercises'),
    path('my_exercises/edit/<int:user_exercise_id>/', main_views.edit_user_uxercise, name='edit_user_exercise')
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
