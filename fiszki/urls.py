from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.urls import path
from django.views.generic.edit import CreateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_set/', views.add_set, name='add_set'),
    path('set/<int:set_id>/', views.view_set, name='view_set'),
    path('set/<int:set_id>/add_flashcard/', views.add_flashcard, name='add_flashcard'),
    path('set/<int:set_id>/review/', views.review_flashcards, name='review_flashcards'),
path('accounts/register/',
        CreateView.as_view(
            template_name='registration/register.html',
            form_class=UserCreationForm,
            success_url='/accounts/login/'
        ),
        name='register'),

]
